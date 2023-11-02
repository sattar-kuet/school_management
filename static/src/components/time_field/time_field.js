/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

import { Component, useState, onWillUpdateProps } from "@odoo/owl";

export class TimeField extends Component {
    setup() {
        this.state = useState({
            time: this.props.value || '',
        });
    }
}

TimeField.template = "owl.TimeField";
TimeField.props = {
    ...standardFieldProps,
};

TimeField.supportedTypes = ["char"];

registry.category("fields").add("time", TimeField);
