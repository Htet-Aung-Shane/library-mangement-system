{
    'name': 'Library',
    'version': '17.0.1.0',
    'license': 'LGPL-3',
    'category': 'Customizations',
    "sequence": 1,
    'summary': 'Manage Students for library management system',
    'complexity': "easy",
    'author': 'MT Tech',
    'website': 'https://mttech-mm.com',
    'installable': True,
    'auto_install': False,
    'application': True,
    'depends': ['base','contacts','website', 'student','onboarding'],
    'images': [
        'static/description/icon.jpg',
    ],
    'data': [
        'security/ir.model.access.csv',  
        'views/book.xml',
        'views/book_category.xml',
        'views/book_author.xml',
        'views/book_rent.xml',
        'views/book_rent_line.xml',
        'views/book_return_line.xml',
        'views/book_return.xml',
        'views/rent_sequence.xml',
        'views/return_sequence.xml',
        'data/library_dashboard.xml',
        'data/onboarding_data.xml',
        'views/dashboard.xml',
        'views/menu.xml', 
    ],
    'assets': {
        'web.assets_frontend': [
            "library/static/src/scss/custom.scss",  # Frontend styles
        ],
        'web.assets_backend': [
            "library/static/src/scss/custom.scss",  # Frontend styles
        ],
    }
}