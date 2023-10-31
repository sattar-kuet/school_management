# -*- coding: utf-8 -*-

from odoo import fields, models


class YearlyHolidayConfig(models.Model):
    _name = 'school_management.yearly.holiday.wizard'
    _description = 'Holiday Config'

    title = fields.Char(string='Title')
    start_date = fields.Char(string='Start Date')
    end_date = fields.Char(string='End Date')

    def next(self):
        pass

    def back(self):
        pass
