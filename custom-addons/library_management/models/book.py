from odoo import models, fields, api


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'name'

    name = fields.Char(string='Book Title', required=True, tracking=True)
    author = fields.Char(string='Author', tracking=True)
    isbn = fields.Char(string='ISBN', copy=False)
    description = fields.Html(string='Description')

    category_id = fields.Many2one(
        'library.category',
        string='Category',
        required=True,
        ondelete='restrict',
        tracking=True
    )

    cover_image = fields.Image(string='Cover Image', max_width=1024, max_height=1024)
    publication_date = fields.Date(string='Publication Date')
    pages = fields.Integer(string='Number of Pages')
    publisher = fields.Char(string='Publisher')
    language = fields.Selection([
        ('en', 'English'),
        ('ru', 'Russian'),
        ('uz', 'Uzbek'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('other', 'Other'),
    ], string='Language', default='en')

    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color Index', related='category_id.color', store=False)

    _sql_constraints = [
        ('isbn_unique', 'unique(isbn)', 'ISBN must be unique!')
    ]
