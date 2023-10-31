# -*- coding: utf-8 -*-

from odoo import fields, models


class WeeklyHolidayConfig(models.Model):
    _name = 'school_management.weekly.holiday'
    _description = 'Weekly Holiday Config'

    weekly_off_days = fields.Many2many('school_management.week.day', string='Week Days')
