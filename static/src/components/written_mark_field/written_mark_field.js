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
            await this._fetchResultConfig();
         })

    }
    get isValidMark(){
       return this.props.value<= this.this.WrittenMaxMark;
    }
    async _fetchResultConfig() {
       try{
        const {exam,subject} = this.props.record.data;
        const exam_id = exam[0];
        const subject_id = subject[0];
        const postData = {
            subject_id: subject_id,
            exam_id: exam_id,
        };
        const response = await fetch('/school_management/result_config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Add any other headers if required
            },
            body: JSON.stringify(postData),
        });
        if (response.ok) {
            const response_json = await response.json();
            this.resultConfig = response_json.result.written_max_mark;
        } else {
            throw new Error('API request failed');
        }
       } catch (error) {
        console.error("Error fetching result configuration:", error);
        return {};
    }
    }
    get WrittenMaxMark() {
        return this.resultConfig; // default to 100 if not found
    }
}

WrittenMarkFieldTree.template = "owl.WrittenMarkField";
WrittenMarkFieldTree.props = {
    ...standardFieldProps,
};

registry.category("fields").add("written_mark_tree", WrittenMarkFieldTree);