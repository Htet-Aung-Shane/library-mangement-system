from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class Book(models.Model):
    _name = "book.rent"
    _description = "Books Renting"

    no = fields.Char (
        'Rent Sequence', size=16, copy=False,
        readonly=True, store=True,
        default=lambda self:
        self.env['ir.sequence'].next_by_code('book.rent'))  
    rent_date = fields.Date('Rent Date')