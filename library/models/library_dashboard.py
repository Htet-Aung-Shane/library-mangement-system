from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError

class TicketsDashboard(models.Model):
    _name = 'library.dashboard'
    _description = 'Library Dashboard'

    name = fields.Char("Library Dashboard")
    student_count = fields.Integer(compute="_compute_student_count")
    book_count = fields.Integer(compute="_compute_book_count")
    book_rent_count = fields.Integer(compute="_compute_book_rent_count")
    book_return_count = fields.Integer(compute='_compute_book_return_count')
    book_to_return_count = fields.Integer(compute='_compute_book_to_return_count')
    author_count = fields.Integer(compute='_compute_author_count')
    category_count = fields.Integer(compute='_compute_category_count')
    
    @api.depends('student_count')
    def _compute_student_count(self):
        for cot in self:
            cot.student_count = self.env['student'].search_count([])
            
    @api.depends('book_count')
    def _compute_book_count(self):
        for cot in self:
            cot.book_count = self.env['book'].search_count([])
            
    @api.depends('book_rent_count')
    def _compute_book_rent_count(self):
        for cot in self:
            cot.book_rent_count = self.env['book.rent.line'].search_count([])
            
    @api.depends('book_return_count')
    def _compute_book_return_count(self):
        for cot in self:
            cot.book_return_count = self.env['book.return.line'].search_count([('return_date', '!=', False)])
            
    @api.depends('book_to_return_count')
    def _compute_book_to_return_count(self):
        for cot in self:
            cot.book_to_return_count = self.env['book.return.line'].search_count([('return_date', '=', False)])
            
    @api.depends('author_count')
    def _compute_author_count(self):
        for cot in self:
            cot.author_count = self.env['book.author'].search_count([])
            
    @api.depends('category_count')
    def _compute_category_count(self):
        for cot in self:
            cot.category_count = self.env['book.category'].search_count([])
            
    def action_book(self):
        return {
            'res_model': 'book',
            'name': _('Books'),
            'type': 'ir.actions.act_window',
            'views': [(False, 'tree'), (False, 'form')]
        }
    
    def action_book_rent(self):
        return {
            'res_model': 'book.rent',
            'name': _('Book Rent'),
            'type': 'ir.actions.act_window',
            'views': [(False, 'tree'), (False, 'form')]
        }
        
    def action_book_return(self):
        return {
            'res_model': 'book.return',
            'name': _('Book Return'),
            'type': 'ir.actions.act_window',
            'views': [(False, 'tree'), (False, 'form')]
        }
