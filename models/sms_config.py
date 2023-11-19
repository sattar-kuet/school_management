from odoo import fields, models


class SmsConfig(models.Model):
    _name = 'sm.sms.config'
    _description = 'SMS Config'

    sms_for_guardian = fields.Text(string='SMS for Guardian', required=True)
    sms_for_teacher = fields.Text(string='SMS for Teacher', required=True)
    guardian_sms = fields.Boolean(string='Guardian SMS')
    teacher_sms = fields.Boolean(string="Teacher SMS")