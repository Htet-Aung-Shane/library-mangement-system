from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class BookRentLine(models.Model):
    _name = "book.rent.line"
    _description = "Line Of Books Renting"
    
    book_id = fields.Many2one('book', string="Book")
    onhand_quantity = fields.Integer("On Hand Quantity", compute="_compute_book_info")
    author_id = fields.Many2one('book.author', string="Author", compute="_compute_book_info")
    category_ids = fields.Many2many("book.category", string="Categories", compute="_compute_book_info")
    @api.onchange('book_id')
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
    rent_date = fields.Date('Rent Date', default=fields.Date.today())
    acceptance_date = fields.Date('Acceptance Date')
    expire_date = fields.Date('Expired Date')
    is_penalty = fields.Boolean('Is Penalty')
    rent_id = fields.Many2one('book.rent', string="Rent")