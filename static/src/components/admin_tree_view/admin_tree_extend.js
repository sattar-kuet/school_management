/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
export class AdminListController extends ListController {
   setup() {
       super.setup();
   }
   OnAddAdmin() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'school_management.admin.wizard',
          name:'Add Admin',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
      });
   }
}
registry.category("views").add("admin_add_button_in_tree", {
   ...listView,
   Controller: AdminListController,
   buttonTemplate: "button_admin.ListView.Buttons",
});