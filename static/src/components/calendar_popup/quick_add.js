/** @odoo-module **/
import { useAutofocus, useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { _lt } from "@web/core/l10n/translation";

import { Component } from "@odoo/owl";

export class CalendarQuickCreate extends Component {
    setup() {
//        this.titleRef = useAutofocus({ refName: "title" });
//        this.notification = useService("notification");
//        this.creatingRecord = false;
          super.setup();
    }

    get dialogTitle() {
        return _lt("New Holiday");
    }
}

CalendarQuickCreate.template = "web.CalendarQuickCreate";
CalendarQuickCreate.components = {
    Dialog,
};
CalendarQuickCreate.props = {
    title: { type: String, optional: true },
    close: Function,
    record: Object,
    model: Object,
    editRecord: Function,
};
