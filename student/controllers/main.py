from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from datetime import datetime
import json
import pdfkit


class LuckDraw(AuthSignupHome):
    @http.route('/my/student', auth='user', website=True, type='http')
    def student_profile(self, page=0, **kw):
        partner_id = request.env.user.partner_id
        profile = request.env['res.partner'].sudo().search([('id','=',partner_id.id)])
        return request.render("student.StudentProfile", {'profile': profile})