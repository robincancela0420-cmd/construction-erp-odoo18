from odoo import fields, models, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        tracking=True
    )

    @api.onchange("project_id")
    def _onchange_project_id(self):
        if self.project_id:
            warehouse = self.env["stock.warehouse"].search(
                [("project_id", "=", self.project_id.id)],
                limit=1
            )

            if warehouse:
                self.picking_type_id = warehouse.in_type_id

    def button_confirm(self):
        result = super().button_confirm()

        for order in self:
            if not order.project_id:
                continue

            for line in order.order_line:
                if not line.product_id:
                    continue

                self.env["construction.project.cost"].create({
                    "project_id": order.project_id.id,
                    "purchase_order_id": order.id,
                    "purchase_order_line_id": line.id,
                    "product_id": line.product_id.id,
                    "quantity": line.product_qty,
                    "unit_cost": line.price_unit
                })

        return result