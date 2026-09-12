{
    'name': 'Equipment Acquisition History',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Assets',
    'summary': 'Historical acquisition records for tools and equipment',
    'depends': [
        'base',
        'project',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/equipment_acquisition_views.xml',
	'views/equipment_acquisition_reporting.xml',
	'views/equipment_acquisition_dashboard.xml',
    ],
    'installable': True,
    'application': True,
}