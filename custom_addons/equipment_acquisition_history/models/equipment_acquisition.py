from odoo import models, fields, api


class EquipmentAcquisition(models.Model):
    _name = 'equipment.acquisition'
    _description = 'Historical Equipment Acquisition'
    _order = 'purchase_date desc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        default='New',
    )

    item = fields.Char(
        string='Item',
        required=True,
    )

    description = fields.Char(
        string='Description / Model',
    )

    brand = fields.Char(
        string='Brand',
    )

    serial_no = fields.Char(
        string='S/N',
    )

    qty_acquired = fields.Float(
        string='Qty Acquired',
        required=True,
        default=1.0,
    )

    unit = fields.Char(
        string='Unit',
        default='unit',
    )

    purchase_date = fields.Date(
        string='Purchase Date',
        required=True,
    )

    acquisition_year = fields.Integer(
        string='Acquisition Year',
        compute='_compute_acquisition_year',
        store=True,
    )

    remarks = fields.Text(
        string='Remarks',
    )

    invoice_no = fields.Char(
        string='Invoice / DR No.',
    )

    supplier = fields.Char(
        string='Supplier',
    )

    unit_cost = fields.Monetary(
        string='Unit Cost',
        currency_field='currency_id',
    )

    amount = fields.Monetary(
        string='Total Acquisition',
        compute='_compute_amount',
        store=True,
        currency_field='currency_id',
    )

    current_qty = fields.Float(
        string='Current Qty',
        default=0.0,
    )

    qty_difference = fields.Float(
        string='Qty Difference',
        compute='_compute_qty_difference',
        store=True,
    )

    project_id = fields.Many2one(
        'project.project',
        string='Project',
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product',
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    @api.depends('purchase_date')
    def _compute_acquisition_year(self):
        for record in self:
            record.acquisition_year = (
                record.purchase_date.year
                if record.purchase_date
                else False
            )

    @api.depends('qty_acquired', 'unit_cost')
    def _compute_amount(self):
        for record in self:
            record.amount = record.qty_acquired * record.unit_cost

    @api.depends('qty_acquired', 'current_qty')
    def _compute_qty_difference(self):
        for record in self:
            record.qty_difference = record.qty_acquired - record.current_qty

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'equipment.acquisition'
                ) or 'New'
        return super().create(vals_list)