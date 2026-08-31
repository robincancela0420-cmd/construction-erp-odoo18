from odoo import fields, models, api
from odoo.exceptions import UserError


class ConstructionMaterialRelease(models.Model):
    _name = "construction.material.release"
    _description = "Construction Material Release"
    _order = "id desc"

    name = fields.Char(
        string="Release No.",
        required=True,
        copy=False,
        readonly=True,
        default="New",
    )

    release_date = fields.Date(
        string="Release Date",
        default=fields.Date.today,
        required=True,
    )

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=True,
    )

    request_id = fields.Many2one(
        "construction.product.request",
        string="Product Request",
        required=True,
    )

    location_id = fields.Many2one(
        "stock.location",
        string="Source Location",
        required=True,
    )

    picking_id = fields.Many2one(
        "stock.picking",
        string="Delivery Order",
        readonly=True,
        copy=False,
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("release", "Released"),
        ],
        string="Status",
        default="draft",
    )

    line_ids = fields.One2many(
        "construction.material.release.line",
        "release_id",
        string="Material Lines",
    )

    def action_release(self):
        self.ensure_one()

        # Find Central Warehouse Delivery Operation Type
        central_warehouse = self.env["stock.warehouse"].search([
            ("name", "=", "Central Warehouse"),
        ], limit=1)

        if not central_warehouse:
            raise UserError(
                "Central Warehous was not found."
            )

        picking_type = self.env["stock.picking_type"].search([
            ("code", "=", "outgoing"),
            ("warehouse_id", "=", central_warehouse.id),
        ], limit=1)

        if not picking_type:
            raise UserError(
                "Central Warehouse Delivery Operation type was not found."
            )

        # Get Project Warehouse
        warehouse = self.env["stock.warehouse"].search([
            ("project_id", "=", self.project_id.id),
        ], limit=1)

        if not warehouse:
            raise UserError(
                "No warehouse assigned to this project."
            )

        project_location = warehouse.lot_stock_id

        if not project_location:
            raise UserError(
                "The project warehouse has no stock location."
            )

        #Create Delivery Order
        picking = self.env["stock.picking"].create({
            "picking_type_id": picking_type.id,
            "location_id": self.location_id.id,
            "location_dest_id": project_location.id,
            "origin": self.name,
        })

        #Create Stock Moves
        for line in self.line_ids:
            self.env["stock.move"].create({
                "name": line.product_id.display_name,
                "product_id": line.product_id.id,
                "product_uom_qty": line.quantity,
                "product_uom": line.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.location_id.id,
                "location_dest_id": project_location.id,
            })

        picking.action_confirm()

        self.picking_id = picking.id
        self.state = "release"

        return {
            "type": "ir.actions.act_window",
            "name": "Delivery Order",
            "res_model": "stock.picking",
            "view_mode": "form",
            "res_id": picking.id
        }