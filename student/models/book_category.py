from odoo import models, fields, api, _
from random import randint

class BookCategory(models.Model):
    _name = 'book.category'
    _description = 'Books Category'

    def _get_default_color(self):
        return randint(1, 11)
    name = fields.Char ('Name')
    color = fields.Integer(string='Color', default=_get_default_color)
    total_qty = fields.Integer(string="Total Quantity")
    active = fields.Boolean(default=True, help="The active field allows you to hide the category without removing it.")
