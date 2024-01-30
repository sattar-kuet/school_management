from odoo import fields, models, api


class TeacherWizard(models.TransientModel):
    _name = 'school_management.teacher.wizard'
    _description = 'Teacher Wizard'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string="Phone", required=True)
    subjects = fields.Many2many("school_management.subject", string='Subjects')
    designation = fields.Many2one("sm.designation", string="Designation")
    attendance_device_user_id = fields.Char()
    sms_number = fields.Char(string="SMS Number")
    batch = fields.Many2one('school_management.batch')


    def add_teacher(self):
        created_teacher = self.env['res.users'].create({
            'name': self.name,
            'phone': self.phone,
            'sms_number': self.sms_number,
            'attendance_device_user_id': self.attendance_device_user_id,
            'designation': self.designation.id
        })

        teacher_group = self.env.ref('school_management.group_school_teacher')
        if teacher_group:
            created_teacher.write({
                'groups_id': [(4, teacher_group.id, 0)]
            })

        action = {
            'name': 'Teacher',
            'domain': [('groups_id.name', '=', 'School Teacher')],
            'view_mode': 'tree',
            'res_model': 'res.users',
            'view_id': self.env.ref('school_management.view_teacher_tree').id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        return action