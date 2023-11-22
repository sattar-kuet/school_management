from odoo import fields, models, api
from datetime import datetime


class StudentAttendance(models.Model):
    _name = 'school_management.attendance'
    _description = 'Student Attendance'

    user = fields.Many2one('res.users', string='Name', required=True)
    present = fields.Boolean(string="Present", Default=False)
    effective_date = fields.Datetime(string="Date", default=lambda self: datetime.today())
    access_id = fields.Integer()
    user_type = fields.Char(string="User Type")

    @api.model
    def create(self, vals):
        created_attendance = super(StudentAttendance, self).create(vals)
        user_type = ''
        if created_attendance.user:
            if created_attendance.user.has_group('school_management.group_school_teacher'):
                user_type = 'Teacher'
            elif created_attendance.user.has_group('school_management.group_school_student'):
                user_type = 'Student'
        created_attendance.user_type = user_type
