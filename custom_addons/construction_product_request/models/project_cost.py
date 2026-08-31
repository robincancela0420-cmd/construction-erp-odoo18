from odoo import api, fields, models

class ProjectCost(models.Model):
    _name = "construction.project.cost"
    _description = "Construction Project Cost"
    _order = "id desc"

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=True,
        ondelete="cascade",
    )

    purchase_order_id = fields.Many2one(
        "purchase.order",
        string="Purchase Order",
        required=True,
    )

    purchase_order_line_id = fields.Many2one(
        "purchase.order.line",
        string="Purchase Order Line",
        required=True,
    )

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
    )

    quantity = fields.Float(
        string="Quantity",
        required=True,
    )

    unit_cost = fields.Float(
        string="Unit Cost",
        required=True,
    )

    total_cost = fields.Float(
        string="Total Cost",
        compute="_compute_total_cost",
        store=True,
    )

    @api.depends("quantity", "unit_cost")
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.quantity * record.unit_cost

    @api.onchange("purchase_order_line_id")
    def _onchange_purchase_order_line_id(self):
        if self.purchase_order_line_id:
            line = self.purchase_order_line_id

            self.purchase_order_id = line.order_id
            self.product_id = line.product_id
            self.quantity = line.product_qty
            self.unit_cost = line.price_unit