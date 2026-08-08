from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError, AccessError
import re

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

	approved_by = fields.Many2one(
		"res.users",
		string="Approved By",
		readonly=True,
	)

	approved_date = fields.Datetime(
		string="Approved Date",
		readonly=True,
	)

	rejected_by = fields.Many2one(
		"res.users",
		string="Rejected By",
		readonly=True,
	)

	rejected_date = fields.Datetime(
		string="Rejected Date",
		readonly=True,
	)

	def action_submit(self):
		self.state = "submitted"

	def _normalize_product_name(self, name):
		# Normalize the product name by removing extra spaces and converting to Uppercase
		if not name:
			return ""
		# Remove extra spaces and convert to Uppercase
		name = name.strip()
		name = re.sub(r'\s+', ' ', name)
		return name.upper()

	def action_approve(self):
		if not self.env.user.has_group(
			"construction_product_request.group_qs_engineer"
		):
			raise AccessError(
				"Only QS Engineers can approve Product Requests."
			)
		self.write({
			"state": "approved",
			"approved_by": self.env.user.id,
			"approved_date": fields.Datetime.now(),
		})

	def action_reject(self):
		if not self.env.user.has_group(
			"construction_product_request.group_qs_engineer"
		):
			raise AccessError(
				"Only QS Engineers can reject Product Requests."
			)
		self.write({
			"state": "rejected",
			"rejected_by": self.env.user.id,
			"rejected_date": fields.Datetime.now(),
		})

	def write(self, vals):
		for record in self:
			if record.state != "draft":
				allowed_fields = {
					"state",
					"approved_by",
					"approved_date",
					"rejected_by",
					"rejected_date",
				}
			if any(field not in allowed_fields for field in vals):
				raise AccessError(
					"This Product Request can no longer be edited after submission."
				)
		return super().write(vals)