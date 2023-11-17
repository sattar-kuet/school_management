# -*- coding: utf-8 -*-

from odoo import fields, models



class HolidayConfig(models.Model):
    _name = 'school_management.holiday'
    _description = 'Holiday Config'

    title = fields.Char(string='Title')
    start_date = fields.Char(string='Start Date')
    end_date = fields.Char(string='End Date')


