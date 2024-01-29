from odoo import models, fields, api, _
import datetime

class AcademicYear(models.Model):
    _name = "academic.year"
    _description = "Class"

    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the category without removing it.",
    )
    name = fields.Char("Academic Year")
    from_date = fields.Date("From")
    to_date = fields.Date("To")

class Batch(models.Model):
    _name = "batch"
    _description = "Batch"

    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the category without removing it.",
    )
    name = fields.Char("Batch Name")    
    code = fields.Char("Code")
    academic_year_id = fields.Many2one('academic.year',string="Academic Year")


class Class(models.Model):
    _name = "class"
    _description = "Class"

    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the category without removing it.",
    )
    name = fields.Char("Class Name")
    image = fields.Binary()
    code = fields.Char("Code")
    batch_id = fields.Many2one('batch', string="Batch")
    # academic_year_id = fields.Char(string='Academic Year', related='batch_id.academic_year_id', readonly=True, store=True)

