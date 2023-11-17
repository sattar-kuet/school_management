/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
export class GuardianListController extends ListController {
   setup() {
       super.setup();
   }
   OnAddGuardian() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'school_management.guardian.wizard',
          name:'Add Teacher',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
      });
   }
}
registry.category("views").add("guardian_add_button_in_tree", {
   ...listView,
   Controller: GuardianListController,
   buttonTemplate: "button_guardian.ListView.Buttons",
});