from odoo import fields, models, api
from datetime import datetime


class Shift(models.Model):
    _name = 'school_management.shift'
    _description = 'Shift'

    name = fields.Char(string='Name')
    end_time = fields.Datetime(string='End Time')
    start_time = fields.Float(string='Time', digits=(4, 2), widget='float_time')

