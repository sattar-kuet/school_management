from odoo import fields, models, api
from odoo.exceptions import UserError


class GuardianWizard(models.TransientModel):
    _name = 'school_management.guardian.wizard'
    _description = 'Guardian Wizard'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string="Phone", required=True)
    sms_number = fields.Char(string="SMS Number")

    def add_guardian(self):
        print("---14---"*11)
        if not self.phone:
            raise UserError("Phone is required and must be unique for login.")

        login = self.phone.strip()
        created_guardian = self.env['res.users'].create({
            'name': self.name,
            'phone': self.phone,
            'sms_number': self.sms_number,
            'login' : login
        })

        guardian_group = self.env.ref('school_management.group_school_guardian')
        if guardian_group:
            created_guardian.write({
                'groups_id': [(4, guardian_group.id, 0)]
            })

        action = {
            'name': 'Guardian',
            'domain': [('groups_id.name', '=', 'School Guardian')],
            'view_mode': 'tree',
            'res_model': 'res.users',
            'view_id': self.env.ref('school_management.view_guardian_tree').id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        return action
