/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { FloatField } from "@web/views/fields/float/float_field"
import { Component, useState, onWillStart, onWillUpdateProps } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class WrittenMarkField extends Component {
    setup() {
        super.setup()
        console.log("Float Field Inherited")
        console.log(this.props)
    }
}

WrittenMarkField.template = "owl.WrittenMarkField";
WrittenMarkField.props = {
    ...standardFieldProps,
};

WrittenMarkField.supportedTypes = ["float"];
WrittenMarkField.components = { FloatField }
registry.category("fields").add("written_mark", WrittenMarkField);

// Separate component for tree views
export class WrittenMarkFieldTree extends WrittenMarkField {
    setup() {
        super.setup();
        console.log("Tree View - Float Field Inherited");
        this.orm = useService("orm")
        onWillStart(async ()=>{
//            this.handleChange = this.handleChange.bind(this);
            this.resultConfig = await this._fetchResultConfig();
         })
    }
    get isValidMark(){
       return this.props.value<= this.this.WrittenMaxMark
    }
//     handleChange(event) {
//        // Get the entered value from the input
//        const enteredValue = event.target.value;
//
//        // Parse the entered value as a number
//        const numericValue = parseFloat(enteredValue);
//
//        // Check if the value is greater than the maximum
//        if (numericValue > this.WrittenMaxMark) {
//            // If greater than the maximum, set the value to the maximum
//            this.props.update(this.WrittenMaxMark);
//        } else {
//            // If within the limit, update the component's value
//            this.props.update(numericValue);
//        }
//     }

    async _fetchResultConfig() {
       try{
       const {exam,subject} = this.props.record.data;
       let exam_id = exam[0];
       let subject_id = subject[0];
        return this.orm.searchRead('school_management.result_config',[
                ['exam', '=', exam_id],
                ['subject', '=', subject_id],
            ],
           ['written_max_mark']
        );
       } catch (error) {
        console.error("Error fetching result configuration:", error);
        return {}; // Return a default value or handle the error appropriately
    }
    }
    get WrittenMaxMark() {
        return this.resultConfig[0]?.written_max_mark || 100; // default to 100 if not found
    }
}

WrittenMarkFieldTree.template = "owl.WrittenMarkField";
WrittenMarkFieldTree.props = {
    ...standardFieldProps,
};

registry.category("fields").add("written_mark_tree", WrittenMarkFieldTree);
