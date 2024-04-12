from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from random import randint

class Book(models.Model):
    _name = "book"
    _description = "Books"

    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the category without removing it.",
    )
    name = fields.Char("Book Name")
    image = fields.Binary()
    isbn = fields.Char("ISBN")
    author_id = fields.Many2one('book.author', string="Author")
    barcode = fields.Char("Barcode")
    total_qty = fields.Integer("Total Quantity")
    onhand_qty = fields.Integer("On Hand Quantity")      
    rent_qty = fields.Integer("Rent Quantity")
    category_ids = fields.Many2many("book.category")