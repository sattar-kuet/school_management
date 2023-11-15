/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { FloatField } from "@web/views/fields/float/float_field"
import { Component, useState, onWillStart, onWillUpdateProps } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class PracticalMarkField extends Component {
    setup() {
        super.setup()
        console.log("Float Field Inherited")
        console.log(this.props)
    }
}

PracticalMarkField.template = "owl.PracticalMarkField";
PracticalMarkField.props = {
    ...standardFieldProps,
};

PracticalMarkField.supportedTypes = ["float"];
PracticalMarkField.components = { FloatField }
registry.category("fields").add("practical_mark", PracticalMarkField);

// Separate component for tree views
export class PracticalMarkFieldTree extends PracticalMarkField {
    setup() {
        super.setup();
        console.log("Tree View - Float Field Inherited");
        this.orm = useService("orm")
        onWillStart(async ()=>{
            this.resultConfig = await this._fetchResultConfig();
         })

    }

    get isValidMark(){
       return this.props.value<= this.this.PracticalMaxMark
    }

    async _fetchResultConfig() {
       try{
       const {exam,subject} = this.props.record.data;
       let exam_id = exam[0];
       let subject_id = subject[0];
        return this.orm.searchRead('school_management.result_config',[
                ['exam', '=', exam_id],
                ['subject', '=', subject_id],
            ],
           ['practical_max_mark']
        );
       } catch (error) {
        console.error("Error fetching result configuration:", error);
        return {}; // Return a default value or handle the error appropriately
    }
    }
    get PracticalMaxMark() {
        return this.resultConfig[0]?.practical_max_mark || 100; // default to 100 if not found
    }
}

PracticalMarkFieldTree.template = "owl.PracticalMarkField";
PracticalMarkFieldTree.props = {
    ...standardFieldProps,
};

registry.category("fields").add("practical_mark_tree", PracticalMarkFieldTree);
