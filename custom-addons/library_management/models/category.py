from odoo import models, fields, api


class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Library Book Category'
    _order = 'sequence, name'

    name = fields.Char(string='Category Name', required=True, translate=True)
    description = fields.Text(string='Description')
    color = fields.Integer(string='Color Index', default=0)
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(string='Active', default=True)

    # Statistics
    book_count = fields.Integer(
        string='Number of Books',
        compute='_compute_book_count',
        store=False
    )

    @api.depends('book_ids')
    def _compute_book_count(self):
        for category in self:
            category.book_count = len(category.book_ids)

    book_ids = fields.One2many('library.book', 'category_id', string='Books')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Category name must be unique!')
    ]
