from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    tin_number = fields.Char(string="TIN Number")
    philhealth_number = fields.Char(string="PhilHealth Number")
    pagibig_number = fields.Char(string="PAG-IBIG Number")
    sss_number = fields.Char(string="SSS Number") 