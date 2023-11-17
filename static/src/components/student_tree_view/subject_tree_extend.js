/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
export class StudentListController extends ListController {
   setup() {
       super.setup();
   }
   OnAddStudent() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'school_management.student.wizard',
          name:'Add Student',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
      });
   }
}
registry.category("views").add("student_add_button_in_tree", {
   ...listView,
   Controller: StudentListController,
   buttonTemplate: "button_student.ListView.Buttons",
});