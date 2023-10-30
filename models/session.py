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

    def create(self, vals):
        action = {
            'name': f'Weekly Holiday',
            'view_mode': 'form',
            'res_model': 'school_management.weekly.holiday',
            'view_id': self.env.ref('school_management.view_weekly_holiday_form').id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        result = super(SessionConfig, self).create(vals)
        action['res_id'] = result.id  # Set the ID of the newly created record in the action

        return action

