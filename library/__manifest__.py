{
    'name': 'Library',
    'version': '16.0.1.0',
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
    'depends': ['base_setup','contacts','website','student'],
    'images': [
        'static/description/icon.jpg',
    ],
    'data': [
        'security/ir.model.access.csv',  
        'views/book.xml',
        'views/book_category.xml',
        'views/book_author.xml',
        'views/book_rent.xml',
        'views/rent_sequence.xml',
        'views/menu.xml', 
    ]
}