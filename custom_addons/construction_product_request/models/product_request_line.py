from odoo import api, fields, models

class ConstructionProductRequestLine(models.Model):
	_name = "construction.product.request.line"
	_description = "Construction Product Request Line"
	_oder = "id"

	request_id = fields.Many2one(
		"construction.product.request",
		string="Product Request",
		required=True,
		ondelete="cascade",
	)

	product_id = fields.Many2one(
		"product.product",
		string="Product",
		required=True,
	)

	description = fields.Char(
		string="Description"
	)

	quantity = fields.Float(
		string="Quantity",
		default=1.0,
		required=True,
	)

	uom_id = fields.Many2one(
		"uom.uom",
		string="Unit",
	)

	def write(self, vals):
		for record in self:
			if record.request_id.state != "draft":
				raise AccessError(
					"Product Request lines cannot be modified after submission."
				)
		return super().write(vals)

	def unlink(self):
		for record in self:
			if record.request_id.state != "draft":
				raise AccessError(
					"Product Request lines cannot be deleted after submission."
				)
		return super().unlink()

	@api.onchange("product_id")
	def _onchange_product_id(self):
		if self.product_id:
			self.description = self.product_id.name
			self.uom_id = self.product_id.uom_id.id