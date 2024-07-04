from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class Student(models.Model):
    _name = "student"
    _description = "Student"

    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the category without removing it.",
    )
    name = fields.Char("Student Name", required=True)
    image = fields.Binary()
    student_id = fields.Char(track_visibility="onchange", string="Student ID")
    email = fields.Char("Email")
    phone_no = fields.Char("Phone No")
    address = fields.Char("Address")
    class_id = fields.Many2one("class")
    batch_id = fields.Many2one("batch")
    academic_year_id = fields.Many2one("academic.year")
    partner_id = fields.Many2one("res.partner", compute="_compute_partner", store=True)
    is_user = fields.Boolean(default=False)
    
    book_rent_ids = fields.One2many(
        comodel_name='student.book.rent.line',
        inverse_name='rent_student_id',
        string='Books',
        ondelete="cascade",
    )

    @api.model
    def create(self, vals):
        partner_vals = {
            "name": vals.get("name"),
            "email": vals.get("email"),
            "phone": vals.get("phone_no"),
        }
        partner = self.env["res.partner"].create(partner_vals)
        vals["partner_id"] = partner.id
        return super(Student, self).create(vals)
    
    @api.constrains("student_id")
    def _check_unique_student_id(self):
        for stu in self:
            if stu.student_id:
                duplicate_stu = self.search(
                    [("student_id", "=", stu.student_id), ("id", "!=", stu.id)]
                )
                if duplicate_stu:
                    raise UserError("Student ID must be unique!")

    @api.depends("name", "email", "phone_no", "student_id")
    def _compute_partner(self):
        for student in self:
            if student.partner_id:
                student.partner_id.name = student.name
                student.partner_id.email = student.email
                student.partner_id.phone = student.phone_no
                student.partner_id.student_id = student.student_id

    def action_create_user(self):
        for student in self:
            if not student.partner_id:
                raise UserError(_("Please create a student first!"))
            if not student.partner_id.user_id:
                user_vals = {
                    "partner_id": student.partner_id.id,
                    "name": student.partner_id.name,
                    "login": student.partner_id.email,
                    "email": student.partner_id.email,
                    "groups_id": [(6, 0, [self.env.ref("base.group_portal").id])],
                }
                user = self.env["res.users"].create(user_vals)
                student.partner_id.write({"user_id": user.id})
                student.is_user = True

    def action_send_invitation(self):
        for student in self:
            if student.partner_id and student.partner_id.user_id:
                student.partner_id.user_id.action_reset_password()
