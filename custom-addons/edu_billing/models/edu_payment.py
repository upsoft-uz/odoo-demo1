
from odoo import api, fields, models

class EduPayment(models.Model):
    _name = "edu.payment"
    _description = "Student Payment"
    _order = "date desc, id desc"

    contract_id = fields.Many2one("edu.contract", string="Контракт", required=True, ondelete="cascade")
    date = fields.Date("Дата", default=fields.Date.context_today, required=True)
    amount = fields.Monetary("Сумма", required=True, currency_field="currency_id")
    method = fields.Char("Метод")
    note = fields.Char("Комментарий")
    state = fields.Selection([('draft','Черновик'),('posted','Проведён')], default='posted', string="Статус")
    currency_id = fields.Many2one("res.currency", related="contract_id.currency_id", store=True, readonly=True)

    def action_post(self):
        for rec in self:
            rec.state = 'posted'
            rec.contract_id.action_recompute_allocation()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records.mapped("contract_id").action_recompute_allocation()
        return records

    def write(self, vals):
        res = super().write(vals)
        self.mapped("contract_id").action_recompute_allocation()
        return res
