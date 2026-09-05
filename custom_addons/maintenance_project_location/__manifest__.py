{
    'name': 'Maintenance Project Location',
    'version': '18.0.1.0.0',
    'category': 'Maintenance',
    'summary': 'Adds project location to maintenance equipment',
    'depends': [
        'maintenance',
        'project',
    ],
    'data': [
        'views/maintenance_equipment_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}