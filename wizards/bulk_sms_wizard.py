from odoo import fields, models, api


class BulkSmsWizard(models.TransientModel):
    _name = 'school_management.bulk.sms.wizard'
    _description = 'Bulk SMS Wizard'

    receiver = fields.Selection([('student','Student'),('phone','Phone')],string='Receiver', required=True)
    phone_number = fields.Text(string='Phone Number')
    students = fields.Many2many('res.users', string="Students", domain=lambda self: [
            ("groups_id", "in", [self.env.ref("school_management.group_school_student").id])])
    message_content = fields.Text(string="Message Content")



    def confirm(self):
        pass

    def cancel(self):
        pass
