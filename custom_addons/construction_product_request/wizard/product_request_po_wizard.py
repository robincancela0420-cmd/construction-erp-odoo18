from odoo import fields, models, api
from odoo.exceptions import UserError, AccessError

class ProductRequestPOWizard(models.TransientModel):
    _name = "construction.product.request.po.wizard"
    _description = "Create Purchase Order from Product Request"

    vendor_id = fields.Many2one(
        "res.partner",
        string="Vendor",
        required=True,
    )

    def action_create_purchase_order(self):
        self.ensure_one()

        if not self.env.user.has_group(
            "construction_product_request.group_procurement"
        ):
            raise AccessError(
                "You do not have the necessary permissions to create a purchase order."
            )

        # Get The Product Request that opened this wizard
        request = self.env["construction.product.request"].browse(
            self.env.context.get("active_id")
        )

        if not request.exists():
            raise UserError("Product Request not found.")

        if request.state != "approved":
            raise UserError(
                "Only approved Product Request can be convereted to Purchase Order."
            )

        if request.purchase_order_id:
            raise UserError(
                "A Purchase Order has already been created for this Product Request."
            )

        # Create Draft Purchase Order
        purchase_order = self.env["purchase.order"].create({
            "partner_id": self.vendor_id.id,
        })

        # Copy Product Request Lines to Purchase Order Lines
        for line in request.line_ids:
            self.env["purchase.order.line"].create({
                "order_id": purchase_order.id,
                "product_id": line.product_id.id,
                "name": line.description or line.product_id.display_name,
                "product_qty": line.quantity,
                "product_uom": line.product_uom.id,
            })

        # Link PR to PO
        request.purchase_order_id = purchase_order.id

        return{
            "type": "ir.actions.act_window",
            "name": "Purchase Order",
            "res_model": "purchase.order",
            "view_mode": "form",
            "res_id": purchase_order.id,
            "target": "current",
        }