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
    student_id = fields.Many2one('student', string="Student")
    return_date = fields.Date('Return Date', default=fields.Date.today())
    total_penalty_fee = fields.Float('Total Penalty Fee')
    is_generate = fields.Boolean('Is Generate', default=False)
    is_return = fields.Boolean('Is Return', default=False)

    @api.onchange('no')
    def _compute_name(self):
        for rec in self:
            if rec.no:
                rec.name = rec.no
            else:
                rec.nmae = False
    
    
    def action_generate(self):
        self.is_generate = True
    
    def action_return(self):
        print('return')
    
    def action_draft(self):
        print('cancel')
        self.is_generate = False