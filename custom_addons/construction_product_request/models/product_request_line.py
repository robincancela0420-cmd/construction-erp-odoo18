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