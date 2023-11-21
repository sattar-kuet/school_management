from odoo import fields, models
from datetime import datetime


class StudentAttendance(models.Model):
    _name = 'school_management.attendance'
    _description = 'Student Attendance'

    user = fields.Many2one('res.users', string='Name', required=True)
    present = fields.Boolean(string="Present", Default=False)
    fields.Datetime(string="Date", default=lambda self: datetime.today())
    access_id = fields.Integer()
