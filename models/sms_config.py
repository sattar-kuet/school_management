from odoo import fields, models


class SmsConfig(models.Model):
    _name = 'sm.sms.config'
    _description = 'SMS Config'

    sms_on_present = fields.Text(string='SMS On Present')
    sms_on_absent = fields.Text(string='SMS on Absent')
    max_delay_on_absent = fields.Integer(string='Max Delay on Absent')
    sms_on_result_publish = fields.Text(string="SMS on Result Publish")