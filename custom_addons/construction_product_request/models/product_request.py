from odoo import api, fields, models

class ConstructionProductRequest(models.Model):
	_name = "construction.product.request"
	_description = "Construction Product Request"
	_inherit = ["mail.thread", "mail.activity.mixin"]
	_order = "id desc"

	name = fields.Char(
		string="Request No",
		required=True,
		copy=False,
		readonly=True,
		default="New",
		tracking=True,
	)

	request_date = fields.Date(
		string="Request Date",
		default=fields.Date.today,
		required=True,
		tracking=True,
	)

	requested_by = fields.Many2one(
		"res.users",
		string="Requested By",
		default=lambda self: self.env.user,
		required=True,
		tracking=True,
	)

	state = fields.Selection(
		[
			("draft", "Draft"),
			("submitted", "Submitted"),
			("approved", "Approved"),
			("rejected", "Rejected"),
		],
		string="Status",
		default="draft",
		tracking=True
	)

	reason = fields.Text(
		string="Reason"
	)

	line_ids = fields.One2many(
		"construction.product.request.line",
		"request_id",
		string="Product Line"
	)