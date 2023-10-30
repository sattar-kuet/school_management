# -*- coding: utf-8 -*-

from odoo import fields, models


class SessionConfig(models.Model):
    _name = 'school_management.session'
    _description = 'Session Config'

    title = fields.Char(string='Title')
    start_year = fields.Char(string='Start Year')
    end_year = fields.Char(string='End Year')

