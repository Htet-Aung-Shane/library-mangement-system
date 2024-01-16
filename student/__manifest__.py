{
    'name': 'Student',
    'version': '16.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 1,
    'summary': 'Manage Students for library management system',
    'complexity': "easy",
    'author': 'MT Tech',
    'website': 'https://mttech-mm.com',
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': [
        'static/description/icon.jpg',
    ],
    'data': [
        'security/ir.model.access.csv',  
        'views/menu.xml', 
        'views/student.xml',
    ]
}