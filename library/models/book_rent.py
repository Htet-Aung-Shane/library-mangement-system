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
    author_ids = fields.Many2many('book.author', string="Authors", compute='_compute_author_ids', store=True)
    category_ids = fields.Many2many("book.category", compute='_compute_category_ids', store=True)
    admin_id = fields.Many2one('res.partner', string="Admin")
    student_id = fields.Many2one('student', string="Student")
    rent_ids = fields.One2many(
        comodel_name='book.rent.line',
        inverse_name='rent_id',
        string='Books',
        required=True,
    )
    is_confirm = fields.Boolean('Is Confirm', default=False)

    @api.model
    def create(self, vals):
        vals["admin_id"] = self.env.user.partner_id.id
        return super(BookRent, self).create(vals)
    
    @api.depends('rent_ids.book_id')
    def _compute_author_ids(self):
        for rec in self:
            if rec.rent_ids:
                rec.author_ids = rec.rent_ids.mapped('book_id.author_id')
            else:
                rec.author_ids = False
    
    @api.depends('rent_ids.book_id')
    def _compute_category_ids(self):
        for rec in self:
            if rec.rent_ids:
                rec.category_ids = rec.rent_ids.mapped('book_id.category_ids')
            else:
                rec.category_ids = False

    def action_confirm(self):
        self.is_confirm = True

    def action_draft(self):
        self.is_confirm = False