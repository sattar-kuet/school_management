from odoo import fields, models, api


class SmsConfigWizard(models.Model):
    _name = 'sm.sms.config.wizard'
    _description = 'SMS Config Wizard'

    sms_on_present = fields.Text(string='SMS On Present')
    help_text_on_present = fields.Text(string='Help Text on Present')
    sms_on_absent = fields.Text(string='SMS on Absent')
    max_delay_on_absent = fields.Text(string='Max Delay on Absent')
    help_text_on_absent = fields.Text(string="Help Text on Absent")
    sms_on_result_publish = fields.Text(string="SMS on Result Publish")
    help_text_on_result_publish = fields.Text(string="Help Text on Result Publish")

    @api.model
    def default_get(self, fields):
        sms_config = self.env['sm.sms.config'].search([], limit=1)
        record = super(SmsConfigWizard, self).default_get(fields)
        if sms_config:
            record['sms_on_present'] = sms_config.sms_on_present
            record['help_text_on_present'] = sms_config.help_text_on_present
            record['sms_on_absent'] = sms_config.sms_on_absent
            record['max_delay_on_absent'] = sms_config.max_delay_on_absent
            record['help_text_on_absent'] = sms_config.help_text_on_absent
            record['sms_on_result_publish'] = sms_config.sms_on_result_publish
            record['help_text_on_result_publish'] = sms_config.help_text_on_result_publish

        return record

    def next(self):
        sms_data = {
            'sms_on_present': self.sms_on_present,
            'help_text_on_present': self.help_text_on_present,
            'sms_on_absent': self.sms_on_absent,
            'max_delay_on_absent': self.max_delay_on_absent,
            'help_text_on_absent': self.help_text_on_absent,
            'sms_on_result_publish': self.sms_on_result_publish,
            'help_text_on_result_publish': self.help_text_on_result_publish,
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