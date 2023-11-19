from odoo import fields, models


class StudentAttendance(models.Model):
    _name = 'sm.student.attendance'
    _description = 'Student Attendance'

    student = fields.Many2one('res.users', string='Student Name', required=True)
    present = fields.Boolean(string="Present", Default= False)
    effective_date = fields.Datetime(string="Date")