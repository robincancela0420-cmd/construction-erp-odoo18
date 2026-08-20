from odoo import models, fields

class WarehouseProject(models.Model):
    _inherit = "stock.warehouse"

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=True,
        tracing=True,
    )