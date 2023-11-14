# -*- coding: utf-8 -*-

from odoo import fields, models, api


class YearlyHolidayConfig(models.Model):
    _name = 'school_management.yearly.holiday.wizard'
    _description = 'Holiday Config'

    name = fields.Char(string='Title')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
