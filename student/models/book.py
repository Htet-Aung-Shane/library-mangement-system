from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from random import randint

class Student(models.Model):
    _name = "book"
    _description = "Books"

    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the category without removing it.",
    )
    name = fields.Char("Book Name")
    image = fields.Binary()
    book_isbn = fields.Char(track_visibility='onchange', string="ISBN")
    Author = fields.Char("Author")
    barcode = fields.Char("Barcode")


    @api.constrains('student_id')
    def _check_unique_student_id(self):
        for stu in self:
            if stu.student_id:
                duplicate_stu = self.search([('student_id', '=', stu.student_id), ('id', '!=', stu.id)])
                if duplicate_stu:
                    raise UserError('Student ID must be unique!!!')
                
    
    class Category(models.Model):
        _name = 'book.category'
        _description = 'Books Category'

        def _get_default_color(self):
            return randint(1, 11)
        name = fields.Char ('Name')
        color = fields.Integer(string='Color', default=_get_default_color)
        active = fields.Boolean(default=True, help="The active field allows you to hide the category without removing it.")

    class Author(models.Model):
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