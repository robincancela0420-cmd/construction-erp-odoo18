from odoo import fields, models

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    project_id = fields.Many2one(
        'project.project',
        string="Project Location",
        help="Project where this equipment is currently located"
    )