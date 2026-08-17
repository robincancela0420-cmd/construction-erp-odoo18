from odoo import fields, models


class ConstructionProject(models.Model):
    _name = "construction.project"
    _description = "Construction Project"
    _order = "id desc"

    name = fields.Char(
        string="Project Name",
        required=True,
        copy=False,
    )

    code = fields.Char(
        string="Project Code",
        required=True,
        copy=False,
    )

    project_manager_id = fields.Many2one(
        "res.users",
        string="Project Manager",
    )

    pic_id = fields.Many2one(
        "res.users",
        string="PIC",
    )

    status = fields.Selection(
        [
            ("active", "Active"),
            ("completed", "Completed"),
            ("on_hold", "On Hold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="active",
        required=True,
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )