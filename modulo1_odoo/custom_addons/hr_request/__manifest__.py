{
    'name': 'Solicitudes Internas de Empleados',

    # Version del modulo siguiendo el formato habitual de Odoo.
    'version': '16.0.1.0.0',

    'author': 'angel garrido',

    'category': 'recursos humanos',

    'summary': 'Gestion de solicitudes internas: vacaciones, permisos, anticipos.',

    # hr aporta empleados; mail permite chatter, seguidores y actividades.
    'depends': ['hr', 'mail'],

    # Archivos cargados al instalar el modulo.
    'data': [
        'security/ir.model.access.csv',
        'security/hr_request_rules.xml',
        'views/hr_request_views.xml',
        'views/hr_request_menus.xml',
    ],

    # Datos opcionales cargados solo cuando la base esta en modo demo.
    'demo': [
        'data/demo_data.xml',
    ],

    'installable': True,

    'auto_install': False,

    'license': 'LGPL-3',
}
