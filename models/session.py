# -*- coding: utf-8 -*-

from odoo import fields, models, api
import datetime


class SessionConfig(models.Model):
    _name = 'school_management.session'
    _description = 'Session Config'
    _rec_name = 'title'

    title = fields.Char(string='Title')
    start_year = fields.Char(string='Start Year')
    end_year = fields.Char(string='End Year')
    status = fields.Selection(
        selection=[('active', 'Active'),
                   ('archive', 'Archive')], string='Status', default='active')

    @api.model
    def default_get(self, fields):
        record = super(SessionConfig, self).default_get(fields)
        current_year = datetime.date.today().year
        next_year = current_year + 1
        current_year = str(current_year)
        next_year = str(next_year)

        record['title'] = f'Session: {current_year} - {next_year}'
        record['start_year'] = current_year
        record['end_year'] = next_year

        return record
