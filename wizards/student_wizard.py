from odoo import fields, models, api


class StudentWizard(models.TransientModel):
    _name = 'school_management.student.wizard'
    _description = 'Student Wizard'

    name = fields.Char(string='Name', required=True)
    roll = fields.Char(string="Roll", required=True)
    blood_group = fields.Selection([
        ('a+', 'A+'),
        ('b+', 'B+'),
        ('ab+', 'AB+'),
    ], string='Blood Group', required=True)
    class_config = fields.Many2one("sm.class_config", string='Class')
    class_has_group = fields.Boolean(compute='_compute_class_has_group')
    student_group = fields.Many2one("school_management.group", string='Group')
    attendance_device_user_id = fields.Char(string='Attendance Device User ID')

    @api.depends('class_config')
    def _compute_class_has_group(self):
        for student in self:
            student.class_has_group = student.class_config.has_group

    def add_student(self):
        created_student = self.env['res.users'].create({
            'name': self.name,
            'roll': self.roll,
            'blood_group': self.blood_group,
            'class_config': self.class_config.id,
            'student_group': self.student_group.id,
            'attendance_device_user_id': self.attendance_device_user_id
        })

        student_group = self.env.ref('school_management.group_school_student')
        if student_group:
            created_student.write({
                'groups_id': [(4, student_group.id, 0)]
            })

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
