from odoo import fields, models, api


class BulkSmsWizard(models.TransientModel):
    _name = 'school_management.bulk.sms.wizard'
    _description = 'Bulk SMS Wizard'

    receiver = fields.Selection([('student','Student'),('phone','Phone')],string='Receiver', required=True)
    phone_number = fields.Text(string='Phone Number')
    students = fields.Many2many('res.users', string="Students", domain=lambda self: [
            ("groups_id", "in", [self.env.ref("school_management.group_school_student").id])])
    message_content = fields.Text(string="Message Content")

    def send(self):
        if self.receiver == 'student':
            for student in self.students:
                self.env['school_management.helper'].send_sms_via_reve_system(student.phone, self.message_content)
        else:
            phones_per_lines = self.phone_number.split('\n')
            for phones_per_line in phones_per_lines:
                comma_seperated_phones = phones_per_line.split(',')
                for comma_seperated_phone in comma_seperated_phones:
                    space_seperated_phones = comma_seperated_phone.split(' ')
                    for space_seperated_phone in space_seperated_phones:
                        phone = space_seperated_phone.strip()
                        self.env['school_management.helper'].send_sms_via_reve_system(phone, self.message_content)

