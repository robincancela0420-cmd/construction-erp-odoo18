{
    "name": "Construction Product Request",
    "version": "18.0.1.0.0",
    "summary": "Product Creation Request Workflow",
    "description": """
Construction Product Request Module

Workflow:
Operations / QS
        ↓
Product Request
        ↓
Product Master Admin
        ↓
Approved
        ↓
Create Product
""",
    "author": "Robin Cancela",
    "website": "",
    "category": "Construction",
    "license": "LGPL-3",

    "depends": [
        "base",
        "mail",
        "product",
        "purchase",
        "stock",
    ],

    "data": [
        "security/security.xml",
    	"security/ir.model.access.csv",
    	"views/product_request_views.xml",
        "views/product_views.xml",
        "views/product_template_views.xml",
        "views/product_request_po_wizard_views.xml"
        

    ],

    "installable": True,
    "application": True,
}