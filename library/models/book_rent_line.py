from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class BookRentLine(models.Model):
    _name = "book.rent.line"
    _description = "Line Of Books Renting"
    
    book_id = fields.Many2one('book', string="Book")
    onhand_quantity = fields.Integer("On Hand Quantity",related='book_id.onhand_qty')
    author_id = fields.Many2one('book.author', string="Author",compute="_onchange_book_info")
    category_ids = fields.Many2many("book.category", string="Categories",compute="_onchange_book_info")
    student_id = fields.Many2one('student', string="Student")
    admin_id = fields.Many2one('res.partner', string="Admin")
    is_confirm = fields.Boolean(string="Confirm",Default=False)

    @api.onchange("book_id")
    def _onchange_book_info(self):
        for rec in self.book_id:
            for book in rec:
                self.onhand_quantity = book.onhand_qty
                self.author_id = book.author_id
                self.category_ids = book.category_ids
    
    rent_quantity = fields.Integer("Rent Quantity")
    rent_date = fields.Date('Rent Date', default=fields.Date.today())
    return_date = fields.Date('Returned Date')
    expire_date = fields.Date('Expired Date')
    is_penalty = fields.Boolean('Is Penalty', compute="_compute_is_penalty",store=True,pre_compute=True)
    rent_id = fields.Many2one('book.rent', string="Rent")
    is_returned = fields.Boolean('Is Returned', default=False)
    is_rent = fields.Boolean('Is Rent', default=False)

    @api.constrains('expire_date', 'rent_date')
    def _check_dates(self):
        for record in self:
            if record.expire_date and record.rent_date and record.expire_date < record.rent_date:
                raise UserError(_("The Expired Date cannot be earlier than the Rent Date."))
            if record.rent_quantity > record.onhand_quantity:
                raise UserError(_("The Rent Quantity cannot be greater than the On Hand Quantity."))

    @api.depends()
    def _compute_is_penalty(self):
        for line in self:
            today = fields.Date.today()
            if line.expire_date > today:
                line.is_penalty = False
            else:
                line.is_penalty = True

    @api.depends('return_date')            
    def _compute_is_returned(self):
        for line in self:
            if line.return_date:
                line.is_returned = True
            else:
                line.is_returned = False