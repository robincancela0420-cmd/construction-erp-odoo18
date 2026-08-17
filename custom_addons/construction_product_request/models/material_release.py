from odoo import fields, models


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
        "construction.project",
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