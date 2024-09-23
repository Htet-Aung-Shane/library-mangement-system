/** @odoo-module **/
import PublicWidget from '@web/legacy/js/public/public_widget';

PublicWidget.registry.Book = PublicWidget.Widget.extend({
    selector: '.book_page_id',
    events: {
        'click #add_rent': 'addBookId', 
        'click .rent_now': 'rentNow' 
        // Changed from 'click' to 'change'
    },
    init: function () {
        this._super(...arguments);
        this.orm = this.bindService("orm");
        this.ary = JSON.parse(localStorage.getItem('bookCount'));
        this.bk_count = [];
        this.comDate = [];
    },

    async start() {
        this._super.apply(this, arguments);  // Ensure parent class `start` is called
        this.getCount()
        const getAllData =await this.orm.searchRead('book',[],['id']);
        if(this.ary.length > 0){
            this.comDate = this.ary
        }
        console.log(getAllData)
    },

    getCount(){
        this.bk_count =this.ary? JSON.parse(localStorage.getItem('bookCount')) : [];
        console.log(this.bk_count,this.ary)
        if(this.bk_count.length > 0){
            console.log("win")
            $('#count_book').html(this.bk_count.length);
            $('.book_id_obj').val(this.bk_count)
            $('#rent_button').removeClass('disabled')
        }else{
            console.log("Null")
            $('#rent_button').addClass('disabled');
            $('#count_book').html(0);
        }

    },

    addBookId(event) {
        const button = $(event.currentTarget); 
        const bookId = button.attr('value');
        const id = JSON.parse(bookId)   
        if (!this.bk_count.includes(id)) { // Check if the book ID already exists
            this.bk_count.push(id);
            button.removeClass('btn-outline-secondary ')
            button.addClass('btn-secondary ') // Add the ID if it doesn't already exist
        }
        if(this.bk_count.length > 0){
            $('.book_id_obj').val(JSON.stringify(this.bk_count))
        }
        console.log("book added",this.bk_count.length)//

        localStorage.setItem('bookCount',JSON.stringify(this.bk_count));

        const book_length = localStorage.getItem('bookCount');
        const obj_book = JSON.parse(book_length)
        if (this.bk_count) {
            console.log(obj_book)
            $('#count_book').html( obj_book.length);
            $('#rent_button').removeClass('disabled')
        }
    },

    rentNow(event){
        const button = $(event.currentTarget); 
        const bookId = button.attr('value');

        console.log("remove id is,",bookId)
    }

});
