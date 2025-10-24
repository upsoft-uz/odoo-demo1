
from odoo import api, fields, models

class EduContract(models.Model):
    _name = "edu.contract"
    _description = "Education Contract"
    _order = "id desc"

    student_id = fields.Many2one("edu.student", string="Студент", required=True, ondelete="cascade")
    name = fields.Char("Номер/Название", required=True, default=lambda self: self._default_name())
    contract_total = fields.Monetary("Сумма контракта", required=True, currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", required=True, default=lambda self: self.env.company.currency_id.id)

    penalty_rate = fields.Float("Пеня (% в день)", default=1.0)  # 1%/день
    installment_ids = fields.One2many("edu.installment", "contract_id", string="Части", copy=True)
    payment_ids = fields.One2many("edu.payment", "contract_id", string="Платежи", copy=True)

    paid_total = fields.Monetary("Оплачено всего", compute="_compute_totals", store=True, currency_field="currency_id")
    penalty_total = fields.Monetary("Пеня всего", compute="_compute_totals", store=True, currency_field="currency_id")
    balance_total = fields.Monetary("Остаток без пени", compute="_compute_totals", store=True, currency_field="currency_id")
    outstanding_with_penalty = fields.Monetary("К оплате (с пеней)", compute="_compute_totals", store=True, currency_field="currency_id")

    @api.model
    def _default_name(self):
        return self.env['ir.sequence'].next_by_code('edu.contract') or "CONTRACT"

    @api.depends("installment_ids.paid_amount", "installment_ids.penalty_amount", "contract_total")
    def _compute_totals(self):
        for rec in self:
            rec.paid_total = sum(rec.installment_ids.mapped("paid_amount"))
            rec.penalty_total = sum(rec.installment_ids.mapped("penalty_amount"))
            rec.balance_total = max(rec.contract_total - rec.paid_total, 0.0)
            rec.outstanding_with_penalty = rec.balance_total + rec.penalty_total

    def action_recompute_allocation(self):
        for rec in self:
            total_paid = sum(p.amount for p in rec.payment_ids if p.state == 'posted' or not p.state)
            remain = total_paid
            for inst in rec.installment_ids.sorted(key=lambda i: i.sequence):
                take = min(inst.due_amount, remain)
                inst.paid_amount = max(take, 0.0)
                inst.balance_amount = max(inst.due_amount - inst.paid_amount, 0.0)
                remain -= take

    def cron_recompute_penalties(self):
        today = fields.Date.today()
        for rec in self.search([]):
            for inst in rec.installment_ids:
                overdue = bool(inst.deadline and inst.deadline < today and inst.balance_amount > 0)
                inst.overdue = overdue
                if overdue:
                    days = (today - inst.deadline).days
                    rate = (rec.penalty_rate or 0.0) / 100.0
                    inst.penalty_amount = round(inst.balance_amount * rate * days, 0)
                else:
                    inst.penalty_amount = 0.0

class EduInstallment(models.Model):
    _name = "edu.installment"
    _description = "Installment"
    _order = "sequence asc"

    contract_id = fields.Many2one("edu.contract", required=True, ondelete="cascade")
    sequence = fields.Integer("№", required=True, default=1)
    label = fields.Char("Метка", help="Например, '1-октябрь'")
    deadline = fields.Date("Дедлайн")
    due_amount = fields.Monetary("План", required=True, currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", related="contract_id.currency_id", store=True, readonly=True)

    paid_amount = fields.Monetary("Оплачено", currency_field="currency_id")
    balance_amount = fields.Monetary("Остаток", currency_field="currency_id")
    penalty_amount = fields.Monetary("Пеня", currency_field="currency_id")
    overdue = fields.Boolean("Просрочено")
