from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class BookReturn(models.Model):
    _name = "book.return"
    _description = "Books Renting"

    no = fields.Char(
        "Return Sequence",
        size=16,
        copy=False,
        readonly=True,
        store=True,
        default="Draft",
    )
    name = fields.Char("Name", compute="_compute_name")
    student_id = fields.Many2one("student", string="Student")
    return_date = fields.Date("Return Date", default=fields.Date.today())
    total_penalty_fee = fields.Float("Total Penalty Fee")
    is_generate = fields.Boolean("Is Generate", default=False)
    is_return = fields.Boolean("Is Return", default=False)
    return_ids = fields.One2many(
        comodel_name="book.return.line",
        inverse_name="return_id",
        string="Returns",
        required=True,
    )

    @api.onchange("no")
    def _compute_name(self):
        for rec in self:
            if rec.no:
                rec.name = rec.no
            else:
                rec.nmae = False

    def action_generate(self):
        # self.is_generate = True
        for rec in self:
            rent_obj = self.env["book.rent.line"].search(
                [("student_id", "=", rec.student_id.id), ("is_rent", "=", True)]
            )
            return_lines = []
            for rent in rent_obj:
                return_lines.append(
                    (
                        0,
                        0,
                        {
                            "rent_line_id": rent.id,
                            "rent_quantity": rent.rent_quantity,
                            "return_quantity": 0,
                            "return_date": rec.return_date,
                            "is_returned": False,
                            "book_id": rent.book_id.id,
                            "student_id": rec.student_id.id,
                            "rent_date": rent.rent_date,
                            "expire_date": rent.expire_date,
                        },
                    )
                )
            if return_lines:
                rec.write({"return_ids": return_lines})

    def action_return(self):
        print("return")

    def action_draft(self):
        for rec in self:
            rec.return_ids = False
            self.is_generate = False
