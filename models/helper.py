from odoo import models
import requests


class Helper(models.AbstractModel):
    _name = 'school_management.helper'

    def pull_attendance_record(self):
        largest_access_id = self.env['school_management.attendance'].search([], order='access_id desc', limit=1)
        access_id = 27774600
        if largest_access_id:
            access_id = largest_access_id.access_id

        end_point = 'https://rumytechnologies.com/rams/json_api'
        pay_load = {
            "operation": "fetch_log",
            "auth_user": "HTRMathematics",
            "auth_code": "h2q6uzc6s6jkb82pygo4fb5ap4fsqpc",
            "start_date": "2023-11-18",
            "end_date": "2023-11-18",
            "start_time": "00:00:00",
            "end_time": "23:59:59",
            "access_id": f"{access_id}"
        }
        response = requests.post(end_point, json=pay_load)
        if response.status_code == 200:
            # Assuming the response is JSON
            response_data = response.json()
            for log in response_data["log"]:

                student = self.env['res.users'].search([('attendance_device_user_id', '=', log['registration_id'])],
                                                       limit=1)
                if student:
                    print('>' * 100, student)
                    self.env['school_management.attendance'].create({
                        'user': student.id,
                        'present': True,
                        'access_id': log['access_id']
                    })
                    if student.guardian:
                        sms_config = self.env['sm.sms.config'].search([], limit=1)
                        if sms_config.guardian_sms:
                            sms_content = sms_config.sms_for_guardian
                            message = sms_content.replace("{student_name}", student.name)
                            response = self.send_normal_sms(student.guardian.phone, message)
                            print(response.text)

    def send_normal_sms(self, phone, message):
        pay_load = {
            'token': 'OJfnlVSqaAzgg61dQWOH',
            'phone': phone,
            'message': message
        }
        end_point = 'https://client.itscholarbd.com/sendsms';
        response = requests.post(end_point, data=pay_load)
        return response

    @staticmethod
    def send_instant_sms(phone, message):
        pay_load = {
            'api_key': 'C200874164d372dc69bd12.25597146',
            'type': 'text',
            'contacts': phone,
            'senderid': '8809601011284',
            'msg': message
        }
        end_point = 'https://msg.elitbuzz-bd.com/smsapi';
        response = requests.post(end_point, data=pay_load)
        return response
