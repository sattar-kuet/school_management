# -*- coding: utf-8 -*-

from odoo import fields, models


class HolidayConfig(models.Model):
    _name = 'school_management.holiday'
    _description = 'Holiday Config'

    title = fields.Char(string='Title')
    start_date = fields.Char(string='Start Date')
    end_date = fields.Char(string='End Date')
    session_id = fields.Many2one(compute='_compute_session_id', string='session')

    def _compute_session_id(self):
        pass
