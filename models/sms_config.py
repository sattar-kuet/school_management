from odoo import fields, models


class SmsConfig(models.Model):
    _name = 'sm.sms.config'
    _description = 'SMS Config'

    sms_on_present = fields.Text(string='SMS On Present')
    help_text_on_present = fields.Text(string='Help Text on Present')
    sms_on_absent = fields.Text(string='SMS on Absent')
    max_delay_on_absent = fields.Text(string='Max Delay on Absent')
    help_text_on_absent = fields.Text(string="Help Text on Absent")
    sms_on_result_publish = fields.Text(string="SMS on Result Publish")
    help_text_on_result_publish = fields.Text(string="Help Text on Result Publish")