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
            this.resultConfig = await this._fetchResultConfig();
         })

    }

    async _fetchResultConfig() {
       try{
       const {exam,subject} = this.props.record.data;
       let exam_id = exam[0];
       let subject_id = subject[0];
       let result_config =  await this.orm.searchRead('school_management.result_config',[
               ['subject', '=', 3]
            ],
           ['written_max_mark','exam','subject'],
           1 // LIMIT
        );
        console.log("sUBJECT id >>>>>>>>>>");
        console.log(subject_id);
       } catch (error) {
        console.error("Error fetching result configuration:", error);
        return {}; // Return a default value or handle the error appropriately
    }
    }
    get WrittenMaxMark() {
        return 100; // default to 100 if not found
    }
}

WrittenMarkFieldTree.template = "owl.WrittenMarkField";
WrittenMarkFieldTree.props = {
    ...standardFieldProps,
};

registry.category("fields").add("written_mark_tree", WrittenMarkFieldTree);