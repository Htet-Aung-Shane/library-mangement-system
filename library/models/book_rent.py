from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class BookRent(models.Model):
    _name = "book.rent"
    _description = "Books Renting"

    no = fields.Char (
        'Rent Sequence', size=16, copy=False,
        readonly=True, store=True,
        default=lambda self:
        self.env['ir.sequence'].next_by_code('book.rent'))  
    rent_date = fields.Date('Rent Date', default=fields.Date.today())
    author_ids = fields.Many2many('book.author', string="Authors")
    category_ids = fields.Many2many("book.category")
    admin_id = fields.Many2one('res.partner', string="Admin")
    student_id = fields.Many2one('student', string="Student")
    rent_ids = fields.One2many(
        comodel_name='book.rent.line',
        inverse_name='rent_id',
        string='Books',
        required=True,
    )

    @api.model
    def create(self, vals):
        vals["admin_id"] = self.env.user.partner_id.id
        return super(BookRent, self).create(vals)