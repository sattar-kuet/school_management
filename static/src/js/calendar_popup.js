odoo.define('school_management.CalendarQuickCreateCustom', function (require) {
    "use strict";
    alert('hello');
    const { CalendarQuickCreate } = require('web.CalendarQuickCreate');

    CalendarQuickCreate.extend({
        // Override or extend the component methods and properties here
        // For example, you can customize the dialog title as follows:
        get dialogTitle() {
            return _lt("Custom New Event");
        },
    });

    return CalendarQuickCreate;
});
