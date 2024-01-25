from odoo import fields, models, api


class AdminWizard(models.TransientModel):
    _name = 'school_management.admin.wizard'
    _description = 'Admin Wizard'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string="Phone", required=True)
    sms_number = fields.Char(string="SMS Number")
    designation = fields.Many2one("sm.designation", string="Designation")
    attendance_device_user_id = fields.Char()

    def add_admin(self):
        created_guardian = self.env['res.users'].create({
            'name': self.name,
            'phone': self.phone,
            'sms_number': self.sms_number,
            'designation': self.designation.id,
            'attendance_device_user_id': self.attendance_device_user_id
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
