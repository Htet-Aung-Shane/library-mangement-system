from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class Student(models.Model):
    _name = "student"
    _description = "Student"

    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the category without removing it.",
    )
    name = fields.Char("Student Name")
    image = fields.Binary()
    student_id = fields.Char(track_visibility='onchange', string="Student ID")
    email = fields.Char("Email")
    phone_no = fields.Char("Phone No")
    address = fields.Char("Address")
    
    @api.constrains('student_id')
    def _check_unique_student_id(self):
        for stu in self:
            if stu.student_id:
                duplicate_stu = self.search([('student_id', '=', stu.student_id), ('id', '!=', stu.id)])
                if duplicate_stu:
                    raise UserError('Student ID must be unique!!!')              

