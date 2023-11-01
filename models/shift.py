from odoo import fields, models, api
from datetime import datetime


class Shift(models.Model):
    _name = 'school_management.shift'
    _description = 'Shift'

    name = fields.Char(string='Name')
    start_time_hh = fields.Integer(placeholder="Hour",  required=True)
    start_time_mm = fields.Integer(placeholder="Minute", required=True)
    end_time = fields.Datetime(string='End Time')
    meridiem = fields.Selection([('am', 'AM'), ('pm', 'PM')], default='am', required=True)
