from odoo import fields, models, api
from datetime import datetime


class Shift(models.Model):
    _name = 'school_management.shift'
    _description = 'Shift'

    name = fields.Char(string='Name', required=True)
    start_time = fields.Char(string='Start Time')
    end_time = fields.Char(string='End Time')

