{
    'name': 'Student',
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
    'depends': ['base','contacts','website','portal'],
    'images': [
        'static/description/icon.jpg',
    ],
    'data': [
        'security/ir.model.access.csv',  
        'views/student.xml',
        'views/academic_year.xml',
        'views/batch.xml',
        'views/class.xml',
        'views/menu.xml', 
        'views/portal.xml', 
    ],
    "assets": {
        'web.assets_frontend': [
            'student/static/src/js/*',
        ]
    }
}