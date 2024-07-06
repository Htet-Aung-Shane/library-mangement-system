from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class BookReturn(models.Model):
    _name = "book.return"
    _description = "Books Renting"

    no = fields.Char (
        'Return Sequence', size=16, copy=False,
        readonly=True, store=True,
        default="Draft")  
    name = fields.Char ('Name', compute="_compute_name")
    return_date = fields.Date('Return Date', default=fields.Date.today())
    total_penalty_fee = fields.Float('Total Penalty Fee')

    
    @api.onchange('no')
    def _compute_name(self):
        for rec in self:
            if rec.no:
                rec.name = rec.no
            else:
                rec.nmae = False
    
    
    def action_generate(self):
        print('generate')
    
    def action_return(self):
        print('return')
    
    def action_cancel(self):
        print('cancel')