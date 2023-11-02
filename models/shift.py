from odoo import fields, models, api
from datetime import datetime


class Shift(models.Model):
    _name = 'school_management.shift'
    _description = 'Shift'

    name = fields.Char(string='Name', required=True)
    start_time = fields.Char(string='Start Time', required=True)
    start_time_am_pm = fields.Char(string='Start Time',compute='_compute_start_time')
    end_time = fields.Char(string='End Time', required=True)
    end_time_am_pm = fields.Char(string='End Time',compute='_compute_end_time')

    def _compute_start_time(self):
        for record in self:
            time_obj = datetime.strptime(record.start_time, "%H:%M")
            record.start_time_am_pm = time_obj.strftime("%I:%M %p")

    def _compute_end_time(self):
        for record in self:
            time_obj = datetime.strptime(record.end_time, "%H:%M")
            record.end_time_am_pm = time_obj.strftime("%I:%M %p")
