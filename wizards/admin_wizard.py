from odoo import fields, models, api


class AdminWizard(models.TransientModel):
    _name = 'school_management.admin.wizard'
    _description = 'Admin Wizard'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string="Phone", required=True)

    def add_admin(self):
        created_guardian = self.env['res.users'].create({
            'name': self.name,
            'phone': self.phone
        })

        guardian_group = self.env.ref('school_management.group_school_admin')
        if guardian_group:
            created_guardian.write({
                'groups_id': [(4, guardian_group.id, 0)]
            })

        action = {
            'name': 'Admin',
            'domain': [('groups_id.name', '=', 'School Admin')],
            'view_mode': 'tree',
            'res_model': 'res.users',
            'view_id': self.env.ref('school_management.view_admin_tree').id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        return action
