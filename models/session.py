# -*- coding: utf-8 -*-

from odoo import fields, models, api
import datetime


class SessionConfig(models.Model):
    _name = 'school_management.session'
    _description = 'Session Config'
    _rec_name = 'title'

    title = fields.Char(string='Title')
    start_year = fields.Integer(string='Start Year')
    end_year = fields.Integer(string='End Year')
    status = fields.Selection(
        selection=[('active', 'Active'),
                   ('archive', 'Archive')], string='Status', default='active')


