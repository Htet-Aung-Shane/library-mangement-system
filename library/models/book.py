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
    name = fields.Char("Book title")
    image = fields.Binary()
    isbn = fields.Char("ISBN")
    author_id = fields.Many2one('book.author', string="Author")
    barcode = fields.Char("Barcode")
    barcode_image = fields.Binary("Barcode")
    total_qty = fields.Integer("Total Quantity")
    onhand_qty = fields.Integer("On Hand Quantity", compute="_compute_onhand")      
    rent_qty = fields.Integer("Rent Quantity")
    category_ids = fields.Many2many("book.category")

    # additional_field
    sequence_no = fields.Char("Sequence No.")
    accession_no = fields.Char("Accession No.")
    call_no = fields.Char("Call No.")
    date = fields.Date("Date")
    publisher = fields.Char("Publisher")
    edition = fields.Char("Edition")
    year = fields.Char("Year")
    rate = fields.Float("Rate")
    book_source = fields.Char("Book Source")
    degree = fields.Char("Degree")
    department = fields.Char("Department")
    roll_no = fields.Char("Roll No.")

    @api.model
    def create(self, vals):
        if 'accession_no' in vals:
            existing_book = self.env['book'].search([('accession_no', '=', vals['accession_no'])], limit=1)
            if existing_book:
                raise UserError('Accession number must be unique')
        return super(Book, self).create(vals)

    @api.onchange('total_qty','rent_qty')
    def _compute_onhand(self):
        for rec in self:
            if rec.total_qty:
                if not rec.rent_qty:
                    rec.onhand_qty = rec.total_qty
                else:
                    rec.onhand_qty = rec.total_qty - rec.rent_qty
            else:
                rec.onhand_qty = 0

