# -*- coding: utf-8 -*-

from odoo import fields, models


class WeekDay(models.Model):
    _name = 'school_management.week.day'
    _description = 'Week Day'

    name = fields.Char(string='Name')
    value = fields.Integer(string='Value')
