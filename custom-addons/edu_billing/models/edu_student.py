
from odoo import api, fields, models

class EduStudent(models.Model):
    _name = "edu.student"
    _description = "Student"
    _order = "name"

    name = fields.Char("ФИО", required=True)
    group = fields.Char("Группа")
    course = fields.Char("Курс")
    phone = fields.Char("Телефон")
    contract_ids = fields.One2many("edu.contract", "student_id", string="Контракты")
