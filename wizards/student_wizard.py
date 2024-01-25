from odoo import fields, models, api
from ..constants import BLOOD_GROUP

class StudentWizard(models.TransientModel):
    _name = 'school_management.student.wizard'
    _description = 'Student Wizard'

    name = fields.Char(string='Name', required=True)
    roll = fields.Char(string="Roll", required=True)
    blood_group = fields.Selection(BLOOD_GROUP, string='Blood Group', required=True)
    class_config = fields.Many2one("sm.class_config", string='Class')
    class_has_group = fields.Boolean(compute='_compute_class_has_group')
    student_group = fields.Many2one("school_management.group", string='Group')
    guardian_name = fields.Char()
    guardian_number = fields.Char()
    sms_number = fields.Char()
    phone = fields.Char()
    attendance_device_user_id = fields.Char(string='Attendance Device User ID')
    batch = fields.Many2one('school_management.batch')

    @api.depends('class_config')
    def _compute_class_has_group(self):
        for student in self:
            student.class_has_group = student.class_config.has_group

    def add_student(self):
        gaurdian_id = self.create_gaurdian()
        created_student = self.env['res.users'].create({
            'name': self.name,
            'roll': self.roll,
            'blood_group': self.blood_group,
            'class_config': self.class_config.id,
            'student_group': self.student_group.id,
            'attendance_device_user_id': self.attendance_device_user_id,
            'phone': self.phone,
            'guardian': gaurdian_id,
            'batch': self.batch.id,
            'sms_number': self.sms_number
        })

        student_group = self.env.ref('school_management.group_school_student')
        if student_group:
            created_student.write({
                'groups_id': [(4, student_group.id, 0)]
            })

        self.add_student_to_batch(created_student.id)

        action = {
            'name': 'Student',
            'domain': [('groups_id.name', '=', 'School Student')],
            'view_mode': 'tree',
            'res_model': 'res.users',
            'view_id': self.env.ref('school_management.view_student_tree').id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        return action
    
    def create_gaurdian(self):
        created_guardian = self.env['res.users'].create({
            'name': self.guardian_name,
            'phone': self.guardian_number
        })
        guardian_group = self.env.ref('school_management.group_school_guardian')
        if guardian_group:
            created_guardian.write({
                'groups_id': [(4, guardian_group.id, 0)]
            })
        return created_guardian.id
    
    def add_student_to_batch(self,student_id):
        student_ids = self.batch.students.ids
        student_ids.append(student_id)
        batch_obj = self.env['school_management.batch'].browse(self.batch.id)
        batch_obj.write({
            'students': [(6, 0, student_ids)]
        })

