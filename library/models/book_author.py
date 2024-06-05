from odoo import models, fields, api, _
class BookAuthor(models.Model):
    _name = 'book.author'
    _description = 'Books Author'

    name = fields.Char('Name')
    image = fields.Binary()
    nick_name = fields.Char('Nick Name')
    country_id = fields.Many2one('res.country',string='Country')
    active = fields.Boolean(default=True)
    gender = fields.Selection(
        selection=[
            ('default', 'Default'), ('male', 'Male'), ('female', 'Female'), ('LGBTQ', 'LGBTQ'), ('rather not to say', 'Rather Not To Say')], default='default')
    
    biography = fields.Text("Biography")
    book_ids = fields.One2many(
        comodel_name='book',
        inverse_name='author_id',
        string='Books',
        required=True,
    )