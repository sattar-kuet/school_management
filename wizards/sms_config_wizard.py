from odoo import fields, models, api


class SmsConfigWizard(models.Model):
    _name = 'sm.sms.config.wizard'
    _description = 'SMS Config Wizard'

    sms_on_present = fields.Text(string='SMS On Present')
    sms_on_absent = fields.Text(string='SMS on Absent')
    max_delay_on_absent = fields.Integer(string='Max Delay on Absent(Minutes)')
    sms_on_result_publish = fields.Text(string="SMS on Result Publish")
    help_text = fields.Text(string="Hints")

    @api.model
    def default_get(self, fields):
        sms_config = self.env['sm.sms.config'].search([], limit=1)
        record = super(SmsConfigWizard, self).default_get(fields)
        if sms_config:
            record['sms_on_present'] = sms_config.sms_on_present
            record['sms_on_absent'] = sms_config.sms_on_absent
            record['max_delay_on_absent'] = sms_config.max_delay_on_absent
            record['sms_on_result_publish'] = sms_config.sms_on_result_publish
        record['help_text'] = '<div class="alert alert-warning">' \
                              '<ul><li><strong>{student_name}</strong></li>' \
                              '<li><strong>{exam_title}</strong></li>' \
                              '<li><strong>{total_mark}</strong></li>' \
                              '<li><strong>{grade_title}</strong></li>' \
                              '<li><strong>{grade_point}</strong></li>' \
                              '</div>'

        return record

    def next(self):
        sms_data = {
            'sms_on_present': self.sms_on_present,
            'sms_on_absent': self.sms_on_absent,
            'max_delay_on_absent': self.max_delay_on_absent,
            'sms_on_result_publish': self.sms_on_result_publish
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
