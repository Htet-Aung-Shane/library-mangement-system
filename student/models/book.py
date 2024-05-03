from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from random import randint

class Book(models.Model):
    _name = "book"
    _description = "Books"

    _sql_constraints = [
        ('unique_isbn', 'unique(isbn)', 'ISBN must be unique.'),
    ]
    
    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the category without removing it.",
    )
    name = fields.Char("Book Name")
    image = fields.Binary()
    isbn = fields.Char("ISBN")
    author_id = fields.Many2one('book.author', string="Author")
    barcode = fields.Char("Barcode")
    barcode_image = fields.Binary("Barcode")
    total_qty = fields.Integer("Total Quantity")
    onhand_qty = fields.Integer("On Hand Quantity", compute="_compute_onhand")      
    rent_qty = fields.Integer("Rent Quantity")
    category_ids = fields.Many2many("book.category")

    @api.onchange('total_qty','rent_qty')
    def _compute_onhand(self):
        if self.total_qty:
            if not self.rent_qty:
                self.onhand_qty = self.total_qty
            else:
                self.onhand_qty = self.total_qty - self.rent_qty
        else:
            self.onhand_qty = 0

