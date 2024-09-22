/* @odoo-module */

import { ConfirmationDialog } from '@web/core/confirmation_dialog/confirmation_dialog';
import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.Rent = publicWidget.Widget.extend({
    selector: '#rent_book_page',
    events: {
        'click #rent_now': 'rentNow'
    },

    init() {
        this._super(...arguments); // Call the parent method to ensure proper initialization
        this.dialog = this.bindService("dialog");
    },
    start() {
        // this.dialog.add(ConfirmationDialog, { body: 'Hello World' });
        return this._super.apply(this, arguments);
    },

    rentNow(event) {
        const button = $(event.currentTarget);
        const bookList = button.attr('value');
        console.log("Book List", bookList)
        if (JSON.parse(bookList).length > 0){
            console.log("shit tl",typeof(bookList))
            $('#rent_now').removeClass('disabled')
            $.ajax({
                url: '/send/data', // Replace with your custom Odoo controller endpoint
                type: 'POST',
                data: JSON.stringify({
                    'book_list': bookList
                }),
                contentType: 'application/json',
                success: (response) => {
                    if (response.result.status === 'success') {
                        this.showSuccessDialog();
                        localStorage.removeItem('bookCount')
                    } else {
                        console.log(response.result)
                        console.log(response)
                    }
                },
                error: function (error) {
                    console.log('Error sending data to Odoo:', error);
                }
            });        
        }else{
            $('#rent_now').addClass('disabled')
            alert("Please Choose Book")
        }
      

    },

    showSuccessDialog(){
        if(this.dialog){
            this.dialog.add(ConfirmationDialog,{
                title : "Successfully Rent Book",
                body : 'See your rent book history',
                confirm: ()=>{
                    console.log("confirm")
                    window.location.href= '/rent/history'
    
                },
                cancel : ()=>{
                    window.location.href= '/'
                    console.log("cancel")
                }
            }
            // ,{
    
            // onClose : ()=>{
            //         console.log("close")
            //         window.location.href= '/my/student'
            //     }
            // }
        
        )
        }else{
            console.log("Not true")
        }
    }

});

