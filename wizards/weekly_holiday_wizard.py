# -*- coding: utf-8 -*-

from odoo import fields, models, api


class WeeklyHolidayConfig(models.Model):
    _name = 'sm.weekly.holiday.wizard'
    _description = 'Weekly Holiday Config'

    weekly_off_days = fields.Many2many('school_management.week.day', string='Week Days')

    @api.model
    def default_get(self, fields):
        holiday = self.env['school_management.weekly.holiday'].search([], limit=1)
        record = super(WeeklyHolidayConfig, self).default_get(fields)
        if holiday:
            record['weekly_off_days'] = holiday.weekly_off_days.ids

        return record

    def next(self):
        holiday_data = {
            'weekly_off_days': self.weekly_off_days.ids
        }

        holiday = self.env['school_management.weekly.holiday'].search([], limit=1)
        if holiday:
            holiday.write(holiday_data)
        else:
            self.env['school_management.weekly.holiday'].create(holiday_data)

        self.env['school_management.yearly.holiday'].generate()

        # action = {
        #     'name': 'Configuration',
        #     'view_mode': 'calendar',
        #     'res_model': 'school_management.yearly.holiday.wizard',
        #     'view_id': self.env.ref('school_management.yearly_holiday_calendar').id,
        #     'type': 'ir.actions.act_window',
        #     'target': 'new',
        # }
        # return action

    def back(self):
        action = {
            'name': 'Configuration',
            'view_mode': 'form',
            'res_model': 'school_management.session.wizard',
            'view_id': self.env.ref('school_management.view_session_wizard_form').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return action
