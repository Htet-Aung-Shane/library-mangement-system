from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class BookReturnLine(models.Model):
    _name = "book.return.line"
    _description = "Line Of Books Return"
    
    book_id = fields.Many2one('book', string="Book")
    onhand_quantity = fields.Integer("On Hand Quantity", compute="_compute_book_info")
    author_id = fields.Many2one('book.author', string="Author", compute="_compute_book_info")
    category_ids = fields.Many2many("book.category", string="Categories", compute="_compute_book_info")
    student_id = fields.Many2one('student', string="Student")
    @api.depends('book_id')
    def _compute_book_info(self):
        if self.book_id:
            self.onhand_quantity = self.book_id.onhand_qty
            self.author_id = self.book_id.author_id
            self.category_ids = self.book_id.category_ids
        else:
            self.onhand_quantity = 0
            self.author_id = False
            self.category_ids = False
    
    rent_quantity = fields.Integer("Rent Quantity")
    return_quantity = fields.Integer("Return Quantity")
    rent_date = fields.Date('Rent Date')
    return_date = fields.Date('Returned Date')
    expire_date = fields.Date('Expired Date')
    is_penalty = fields.Boolean('Is Penalty', compute="_compute_is_penalty",store=True,pre_compute=True)
    rent_line_id = fields.Many2one('book.rent.line', string="Rent")
    return_id = fields.Many2one('book.return', string="Return")
    is_returned = fields.Boolean('Is Returned')
    penalty_fee = fields.Float('Penalty Fee')
    
    
    @api.depends('return_date','expire_date')
    def _compute_is_penalty(self):
        for line in self:
            today = fields.Date.today()
            if line.expire_date > today:
                line.is_penalty = False
            else:
                line.is_penalty = True