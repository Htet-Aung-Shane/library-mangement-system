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
    student_id = fields.Char(track_visibility="onchange", string="Student ID")
    email = fields.Char("Email")
    phone_no = fields.Char("Phone No")
    address = fields.Char("Address")
    class_id = fields.Many2one("class")
    batch_id = fields.Many2one("batch")
    academic_year_id = fields.Many2one("academic.year")
    partner_id = fields.Many2one("res.partner", compute="_compute_partner", store=True)
    is_user = fields.Boolean(default=False)

    @api.constrains("student_id")
    def _check_unique_student_id(self):
        for stu in self:
            if stu.student_id:
                duplicate_stu = self.search(
                    [("student_id", "=", stu.student_id), ("id", "!=", stu.id)]
                )
                if duplicate_stu:
                    raise UserError("Student ID must be unique!!!")

    @api.depends("name", "email", "phone_no", "student_id")
    def _compute_partner(self):
        if self.partner_id:
            self.partner_id.name = self.name
            self.partner_id.email = self.email
            self.partner_id.phone = self.phone_no
            self.partner_id.student_id = self.student_id
        else:
            name = self.name or 'Draft'
            self.partner_id = self.env["res.partner"].create(
                {
                    "name": name,
                    "email": self.email,
                    "phone": self.phone_no,
                    "student_id": self.student_id,
                }
            )

    def action_create_user(self):
        if not self.partner_id:
            raise UserError(_("Please create a student first !"))
        if not self.partner_id.user_id:
            user_vals = {
                "partner_id": self.partner_id.id,
                "name": self.partner_id.name,
                "login": self.partner_id.email,
                "email": self.partner_id.email,
                "groups_id": [(6, 0, [self.env.ref("base.group_portal").id])],
            }
            user = self.env["res.users"].create(user_vals)
            self.partner_id.write({"user_id": user.id})
            self.is_user = True

    def action_send_invitation(self):
        if self.partner_id and self.partner_id.user_id:
            self.partner_id.user_id.action_reset_password()
