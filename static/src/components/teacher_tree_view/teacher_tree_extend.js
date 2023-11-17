/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
export class TeacherListController extends ListController {
   setup() {
       super.setup();
   }
   OnAddTeacher() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'school_management.teacher.wizard',
          name:'Add Teacher',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
      });
   }
}
registry.category("views").add("teacher_add_button_in_tree", {
   ...listView,
   Controller: TeacherListController,
   buttonTemplate: "button_teacher.ListView.Buttons",
});