from odoo import fields, models, api, _

class InheritPartner(models.Model):
    _inherit = 'res.partner'
    
    student_id = fields.Char(string="Student ID")