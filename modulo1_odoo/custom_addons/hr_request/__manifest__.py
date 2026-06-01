{
    'name': 'Solicitudes Internas de Empleados',

    'version': '16.0.1.0.0',

    'author': 'angel garrido',

    'category': 'recursos humanos',

    'summary': 'Gestion de solicitudes internas: vacaciones, permisos, anticipos.',

    'depends': ['hr', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'security/hr_request_rules.xml',
        'views/hr_request_views.xml',
        'views/hr_request_menus.xml',
    ],

    'demo': [
        'data/demo_data.xml',
    ],

    'installable': True,

    'auto_install': False,

    'license': 'LGPL-3',
}