from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from datetime import datetime


class Library(AuthSignupHome):
    @http.route("/my/student", auth="user", website=True, type="http")
    def student_profile(self, page=0, **kw):
        partner_id = request.env.user.partner_id
        profile = request.env["res.partner"].sudo().search([("id", "=", partner_id.id)])
        student = (
            request.env["student"].sudo().search([("partner_id", "=", partner_id.id)])
        )
        book_rent = (
            request.env["book.rent.line"]
            .sudo()
            .search([("student_id", "=", student.id), ("is_rent", "=", True)])
        )
        print("book_rent>>>", book_rent)
        return request.render(
            "student.StudentProfile", {"data": book_rent, "profile": profile}
        )

    @http.route("/my/book/rent", auth="user", website=True, type="http")
    def book_rent(self, page=0, **kw):
        books = request.env["book"].sudo().search([])
        categories = request.env["book.category"].sudo().search([])
        authors = request.env["book.author"].sudo().search([])
        partner_id = request.env.user.partner_id
        choose_category = False
        student = (
            request.env["student"].sudo().search([("partner_id", "=", partner_id.id)])
        )
        profile = request.env["res.partner"].sudo().search([("id", "=", partner_id.id)])
        if request.httprequest.method == "POST":
            remark = ""
            qty = 0
            book_id = 0
            author = 0
            catgory = 0

            for key, value in kw.items():
                if key == "author" or key == "category":
                    choose_category = True
                if key == "author":
                    author = value
                if key == "category":
                    category = value
                if key == "remark":
                    remark = value
                elif key == "qty":
                    qty = int(value)
                elif key == "book":
                    book_id = int(value)
            if choose_category:
                if book_id == 0:
                    query = []
                    if author:
                        query.append(('author_id', '=', author))
                    if category:
                        query.append(('category_ids', 'in', [category]))
                    books = request.env["book"].sudo().search(query)

                    return request.render(
                        "student.BookRent",
                        {
                            "books": books,
                            "authors": authors,
                            "categories": categories,
                            "profile": profile,
                            "form_submit": False,
                            "choose_category": choose_category,
                        },
                    )
                else:
                    rent_lines = [
                        (
                            0,
                            0,
                            {
                                "book_id": book_id,
                                "rent_quantity": qty,
                            },
                        )
                    ]

                    rent_data = {
                        "student_id": student.id,
                        "admin_id": partner_id.id,
                        "remark": remark,
                        "rent_ids": rent_lines,
                    }

                    rent = request.env["book.rent"].sudo().create(rent_data)
            return request.render(
                "student.BookRent",
                {
                    "books": books,
                    "authors": authors,
                    "categories": categories,
                    "profile": profile,
                    "form_submit": True,
                    "choose_category": choose_category,
                },
            )

        else:
            return request.render(
                "student.BookRent",
                {
                    "books": books,
                    "profile": profile,
                    "authors": authors,
                    "categories": categories,
                    "profile": profile,
                    "form_submit": False,
                },
            )
