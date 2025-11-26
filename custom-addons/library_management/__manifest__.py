{
    'name': 'Library Management',
    'version': '19.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Simple library book catalog management',
    'description': """
        Library Management System
        ==========================

        A simple demo application for managing library books and categories.

        Key Features:
        -------------
        * Manage books with detailed information
        * Organize books by categories
        * Drag and drop books between categories
        * Color-coded categories
        * Book cover images
    """,
    'author': 'Upsoft',
    'website': 'https://odoo-islomjon.upsoft.app',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/book_views.xml',
        'views/category_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'library_management/static/src/css/library.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
