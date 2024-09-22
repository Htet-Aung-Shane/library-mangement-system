from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from datetime import datetime
import json
import ast

class Library(CustomerPortal):
    @http.route(['/rent_book', '/rent_book/page/<int:page>'], type='http', auth="user", website=True)
    def portal_recruitment(self,page=1,search="",search_in="All",**kw):
        search_list = {
            'All':{'label':'All','input':'All','domain':[]},
            'Name':{'label':'Name', 'input':'Name','domain':[('name','ilike',search)]},
            'Author':{'label':'Author','input':'Author','domain':[('author_id.name','ilike',search)]},
            'Category':{'label':'Category','input':'Category','domain':[('category_ids.name','ilike',search)]}
        }
        search_domain = search_list[search_in]['domain']
        book_obj = request.env['book']
        total_books = book_obj.search_count(search_domain)
        page_details= pager(url="/rent_book",
                            total=total_books,
                            page=page,
                            url_args={'search_in':search_in,'search':search},
                            step=20)
        books = book_obj.search(search_domain,limit=20,offset=page_details['offset'])
        print("pager is ", books,search_domain)

        vals = {'books':books,'page_name':'book_cat','pager':page_details,'search_in':search_in,'searchbar_inputs':search_list,'search':search}
        return request.render("student.rent_book_page",vals)
    
        
    @http.route(["/rent/history", "/rent/history/page/<int:page>"], auth="user", website=True, type="http")
    def student_profile(self, page=1, search=None, search_in='All',**kw):
        search_list = {
            'All':{'label':'All','input':'All','domain':[]},
            'Name':{'label':'Name', 'input':'Name','domain':[('book_id.name','ilike',search)]},
        }
        search_domain = search_list[search_in]['domain']
        profile = request.env["res.partner"].sudo().search([("id", "=", request.env.user.partner_id.id)])
        student = ( request.env["student"].sudo().search([("partner_id", "=", request.env.user.partner_id.id)]) )
        book_rent = (
            request.env["book.rent.line"]
            .sudo()
            .search([("student_id", "=", student.id)], order="create_date desc")
        )
        total_rent_books = book_rent.search_count(search_domain)
        page_details= pager(url="/rent_book",
                            total=total_rent_books,
                            page=page,
                            url_args={'search_in':search_in,'search':search},
                            step=20)
        rent_books =  request.env["book.rent.line"].search(search_domain,limit=20,offset=page_details['offset'], order="create_date desc")
        vals = {'data':rent_books,'page_name':'rent_book','pager':page_details,'search_in':search_in,'searchbar_inputs':search_list,'search':search}

        print("book_rent>>>", rent_books)
        return request.render(
            "student.StudentProfile", vals
        )
    

    @http.route(['/book/views', '/book/views/<int:id>'], type='http', auth="user", website=True)
    def book_view(self,id=None,**post):
        if request.httprequest.method == "POST" and id == None:
            book_list = post.get('book_list')
            if book_list:
                book_list = ast.literal_eval(book_list)
                print("Set book lis is ,,,,",book_list,type(book_list))
                self._set_2_session(book_list)
                res_obj =[]
                for id in book_list:
                    result = request.env['book'].search([('id','=',id)])
                    res_obj.append({
                        'name':result.name,
                        'id':result.id,
                        'author':result.author_id.name,
                        'category':result.category_ids.name,
                        'img':result.image
                    })

                vals  = {'books':res_obj}
                return request.render('student.confirm_rent_book',vals)
        else:
            book_list = self._get_from_session()
            print("Get session is",book_list)
            res_obj =[]
            if id in book_list:
                index = book_list.index(id)
                del book_list[index]

                for bid in book_list:
                    result = request.env['book'].search([('id','=',bid)])
                    res_obj.append({
                        'name':result.name,
                        'id':result.id,
                        'author':result.author_id.name,
                        'category':result.category_ids.name,
                        'img':result.image
                    })
            vals  = {'books':res_obj}
            self._set_2_session(book_list)
            return request.render('student.confirm_rent_book',vals)
    
    def _set_2_session(self,data):
        print("inside set session is 9999999",data,type(data))
        request.session['book_list'] = data


    def _get_from_session(self):
        data = request.session.get('book_list', [])
        print("get data is >>>>>>>>>>>>>>>>>>>>>>",data,type(data))
        return list(data)
    
    @http.route('/send/data',type="json",auth="user",methods=["POST"])
    def submit_books(self, **kw):
        data = json.loads(request.httprequest.data.decode("utf-8"))
        res = self._book_rent(data)
        if res:
            return { 'status': 'success', 'message': 'Successfully Rent'}
        else:
            return {'status':'error'}


    def _book_rent(self,data):
        data_list = ast.literal_eval(data['book_list'])
        student = (
            request.env["student"].sudo().search([("partner_id", "=", request.env.user.partner_id.id)])
        )        
        book_rent, book = request.env['book.rent'], request.env['book']
        book_line_obj= [(0,0,{'book_id':book.sudo().search([('id','=',id)]).id,'student_id':student.id}) for id in data_list]
        vals = {'student_id':student.id,'rent_ids':book_line_obj}
        res = book_rent.sudo().create(vals)
        if res:
            return True if res else False

    
    
    def store_data(self,data = []):
        print("store data is ",data)
        return data