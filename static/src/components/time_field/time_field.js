/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { CharField } from "@web/views/fields/char/char_field"
import { Component, useState, onWillUpdateProps } from "@odoo/owl";

export class TimeField extends Component {
    setup() {
        super.setup()
        console.log("Char Field Inherited")
        console.log(this.props)
    }
}

TimeField.template = "owl.TimeField";
TimeField.props = {
    ...standardFieldProps,
};

TimeField.supportedTypes = ["char"];
TimeField.components = { CharField }
registry.category("fields").add("time", TimeField);
