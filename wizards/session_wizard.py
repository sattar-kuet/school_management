# -*- coding: utf-8 -*-

from odoo import fields, models, api
import datetime


class SessionConfig(models.Model):
    _name = 'school_management.session.wizard'
    _description = 'Session Config'
    _rec_name = 'title'

    title = fields.Char(string='Title')
    start_year = fields.Char(string='Start Year')
    end_year = fields.Char(string='End Year')

    @api.onchange('start_year', 'end_year')
    def _compute_title(self):
        if self.start_year and self.end_year:
            title = f'Session: {self.start_year} - {self.end_year}'
            self.title = title
    @api.model
    def default_get(self, fields):
        session = self.env['school_management.session'].search([
            ('status', '=', 'active'),
        ], limit=1)
        if session:
            current_year = session.start_year
            next_year = session.end_year
            current_year = str(current_year)
            next_year = str(next_year)
            title = session.title
        else:
            current_year = datetime.date.today().year
            next_year = current_year + 1
            current_year = str(current_year)
            next_year = str(next_year)
            title = f'Session: {current_year} - {next_year}'

        record = super(SessionConfig, self).default_get(fields)
        record['title'] = title
        record['start_year'] = current_year
        record['end_year'] = next_year

        return record

    def next(self):
        session_data = {
            'title': self.title,
            'start_year': self.start_year,
            'end_year': self.end_year
        }

        session = self.env['school_management.session'].search([
            ('start_year', '=', self.start_year),
            ('end_year', '=', self.end_year)
        ])
        if session:
            session.write(session_data)
        else:
            self.env['school_management.session'].search([
                ('status', '=', 'active'),
            ]).write({
                'status': 'archive'
            })
            self.env['school_management.session'].create(session_data)

        action = {
            'name': 'Configuration',
            'view_mode': 'form',
            'res_model': 'sm.weekly.holiday.wizard',
            'view_id': self.env.ref('school_management.view_weekly_holiday_wizard_form').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return action
