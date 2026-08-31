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

	project_id = fields.Many2one(
		"project.project",
		string="Project",
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

	purchase_order_id = fields.Many2one(
		"purchase.order",
		string="Purchase Order",
		readonly=True,
		copy=False,
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

	def action_create_purchase_order(self):
		if not self.env.user.has_group(
			"construction_product_request.group_procurement"
		):
			raise AccessError(
				"Only Procurement users can create Purchase Orders."
			)

		if self.purchase_order_id:
			raise UserError(
				"A Purchase Order has already been created for this Product Request."
			)

		warehouse = self.env["stock.warehouse"].search(
			[("project_id", "=", self.project_id.id)],
			limit=1,
		)

		purchase_order = self.env["purchase.order"].create({
			"origin": self.name,
			"partner_id": self.env.user.company_id.partner_id.id,
			"project_id": self.project_id.id,
			"picking_type_id": warehouse.in_type_id.id,
			"order_line": [
				(0, 0, {
					"product_id": line.product_id.id,
					"name": line.description,
					"product_qty": line.quantity,
					"product_uom": line.uom_id.id,
					"price_unit": line.product_id.standard_price,
				}) for line in self.line_ids
			],
		})

		self.with_context(skip_pr_lock=True).write({
			"purchase_order_id": purchase_order.id,
		})

	def write(self, vals):
		if not self.env.context.get("skip_pr_lock"):
			for record in self:
				if record.state != "draft":
					allowed_fields = {
						"state",
						"approved_by",
						"approved_date",
						"rejected_by",
						"rejected_date",
			}

			for record in self:
				if record.state != "draft":
					if any(field not in allowed_fields for field in vals):
						raise AccessError(
							"This Product Request can no longer be edited after submission"
						)
		return super().write(vals)
