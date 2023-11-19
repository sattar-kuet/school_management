# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StudentPromotionConfigWizard(models.Model):
    _name = 'sm.student.promotion.config.wizard'
    _description = 'Student Promotion Config'

    type = fields.Selection([('auto_x', 'Auto in all Class'),
                             ('auto_p', 'Auto if Pass'),
                             ('manual', 'Manual')], string='Title', required=True)



    @api.model
    def default_get(self, fields):
        promotion_type = self.env['sm.student.promotion.config'].search([], limit=1)
        record = super(StudentPromotionConfigWizard, self).default_get(fields)
        if promotion_type:
            record['type'] = promotion_type.type
        return record


    def next(self):
        pass
        type_data = {
            'type': self.type
        }

        promotion_type = self.env['sm.student.promotion.config'].search([], limit=1)
        if promotion_type:
            promotion_type.write(type_data)
        else:
            self.env['sm.student.promotion.config'].create(type_data)

        action = {
            'name': 'Configuration',
            'view_mode': 'form',
            'res_model': 'sm.sms.config.wizard',
            'view_id': self.env.ref('school_management.view_sms_config_wizard_form').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return action

    def back(self):
        action = {
            'name': 'Configuration',
            'view_mode': 'form',
            'res_model': 'sm.weekly.holiday.wizard',
            'view_id': self.env.ref('school_management.view_weekly_holiday_wizard_form').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return action