# -*- coding: utf-8 -*-

from odoo import fields, models


class WeeklyHolidayConfig(models.Model):
    _name = 'sm.weekly.holiday.wizard'
    _description = 'Weekly Holiday Config'

    week_days = fields.Many2many('school_management.week.day', string='Week Days')
