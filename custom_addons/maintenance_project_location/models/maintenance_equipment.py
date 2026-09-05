from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    product_id = fields.Many2one(
        'product.product',
        string="Product",
        help="Product represented by this equipment/tool."
    )

    project_id = fields.Many2one(
        'project.project',
        string="Project Location",
        help="Project where this equipment is currently located"
    )

    @api.onchange('product_id', 'serial_no')
    def _onchange_name_from_product_serial(self):
        for equipment in self:
            product_name = equipment.product_id.display_name or ''
            serial = equipment.serial_no or ''

            if product_name and serial:
                equipment.name = f"{product_name} - {serial}"
            elif product_name:
                equipment.name = product_name