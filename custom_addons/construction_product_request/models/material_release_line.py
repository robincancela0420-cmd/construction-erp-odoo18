from odoo import api, fields, models


class ConstructionMaterialReleaseLine(models.Model):
    _name = "construction.material.release.line"
    _description = "Construction Material Release Line"
    _order = "id"

    release_id = fields.Many2one(
        "construction.material.release",
        string="Material Release",
        required=True,
        ondelete="cascade",
    )

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
    )

    quantity = fields.Float(
        string="Quantity",
        required=True,
        default=1.0,
    )

    uom_id = fields.Many2one(
        "uom.uom",
        string="Unit",
        required=True,
    )

    description = fields.Char(
        string="Description",
    )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.uom_id = self.product_id.uom_id