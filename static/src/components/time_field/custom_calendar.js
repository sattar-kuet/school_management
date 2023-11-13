odoo.define('school_management.custom_calendar', function (require) {
    "use strict";

    var CalendarView = require('web_calendar.CalendarView');
    var Dialog = require('web.Dialog');
    var core = require('web.core');

    CalendarView.include({
        render_event: function(event) {
            var self = this;
            var $event = this._super.apply(this, arguments);

            // Disable the default quick add popup
            $event.find('.fc-day').off('click.quick_add');

            // Attach a custom click event to the date element within the event
            $event.find('.fc-day').click(function () {
                var date = $(this).data('date');
                self.openCustomWizard(date);
            });

            return $event;
        },

        openCustomWizard: function (date) {
            var self = this;
            var wizard = new Dialog(this, {
                title: 'Custom Wizard',
                buttons: [
                    {
                        text: 'Confirm',
                        classes: 'btn-primary',
                        click: function () {
                            // Add your custom logic here
                            wizard.close();
                        }
                    },
                    {
                        text: 'Cancel',
                        classes: 'btn-secondary',
                        close: true
                    }
                ],
            });

            // Customize the content of your wizard here
            wizard.open();
        }
    });
});
