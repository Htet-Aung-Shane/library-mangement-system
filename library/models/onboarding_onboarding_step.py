from odoo import _, api, models


class OnboardingStep(models.Model):
    _inherit = 'onboarding.onboarding.step'

    @api.model
    def action_book(self):
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'book',
            'name': _('Books'),
            'views': [(self.env.ref("library.bok_view_form").id, 'form')],
        }
        return action

    @api.model
    def action_book_rent(self):
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'book.rent',
            'name': _('Rent'),
            'views': [(self.env.ref("library.bok_rent_view_form").id, 'form')],
        }
        return action

    @api.model
    def action_book_return(self):
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'book.return',
            'name': _('Return'),
            'views': [(self.env.ref("library.bok_return_form").id, 'form')],
        }
        return action