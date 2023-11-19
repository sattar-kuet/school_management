from odoo import fields, models, api


class SmsConfigWizard(models.Model):
    _name = 'sm.sms.config.wizard'
    _description = 'SMS Config Wizard'

    sms_for_guardian = fields.Text(string='SMS for Guardian', required=True)
    sms_for_teacher = fields.Text(string='SMS for Teacher', required=True)
    guardian_sms = fields.Boolean(string='Guardian SMS')
    teacher_sms = fields.Boolean(string="Teacher SMS")

    @api.model
    def default_get(self, fields):
        sms_config = self.env['sm.sms.config'].search([], limit=1)
        record = super(SmsConfigWizard, self).default_get(fields)
        if sms_config:
            record['sms_for_guardian'] = sms_config.sms_for_guardian
            record['sms_for_teacher'] = sms_config.sms_for_teacher
            record['guardian_sms'] = sms_config.guardian_sms
            record['teacher_sms'] = sms_config.teacher_sms

        return record

    def next(self):
        sms_data = {
            'sms_for_guardian': self.sms_for_guardian,
            'sms_for_teacher': self.sms_for_teacher,
            'guardian_sms': self.guardian_sms,
            'teacher_sms': self.teacher_sms,
        }

        sms = self.env['sm.sms.config'].search([], limit=1)
        if sms:
            sms.write(sms_data)
        else:
            self.env['sm.sms.config'].create(sms_data)

        # action = {
        #     'name': 'Configuration',
        #     'view_mode': 'form',
        #     'res_model': 'sm.student.promotion.config.wizard',
        #     'view_id': self.env.ref('school_management.view_student_promotion_config_wizard_form').id,
        #     'type': 'ir.actions.act_window',
        #     'target': 'new',
        # }
        # return action

    def back(self):
        action = {
            'name': 'Configuration',
            'view_mode': 'form',
            'res_model': 'sm.student.promotion.config.wizard',
            'view_id': self.env.ref('school_management.view_student_promotion_config_wizard_form').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return action