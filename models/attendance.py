from odoo import fields, models
from datetime import datetime


class StudentAttendance(models.Model):
    _name = 'school_management.attendance'
    _description = 'Student Attendance'

    user = fields.Many2one('res.users', string='Name', required=True)
    present = fields.Boolean(string="Present", Default=False)
    effective_date = fields.Datetime(string="Date", default=lambda self: datetime.today())
    access_id = fields.Integer()
    user_type = fields.Char('res.users', string="User Type", compute='_compute_user_type', store= True)


    def _compute_user_type(self):
        for record in self:
            user_type = ''
            if record.user:
                if record.user.has_group('school_management.group_school_teacher'):
                    user_type = 'teacher'
                elif record.user.has_group('school_management.group_school_student'):
                    user_type = 'student'
            record.user_type = user_type