/** @odoo-module **/
import PublicWidget from '@web/legacy/js/public/public_widget';

PublicWidget.registry.Ticket = PublicWidget.Widget.extend({
    selector: '#book_rent',
    events: {
        'change #author': 'selectAuthor',  // Changed from 'click' to 'change'
    },

    init: function () {
        this._super(...arguments);
        this.orm = this.bindService("orm");
    },

    async start() {
        // Additional initialization logic, if needed
    },

    selectAuthor(event) {
        const authorSelect = $(event.currentTarget);  // Use `event.currentTarget` for the event's source element
        const selectedAuthor = authorSelect.val();  // Get the value of the select box
        console.log('Selected Author:', selectedAuthor);  // Log the selected value
    },
});
