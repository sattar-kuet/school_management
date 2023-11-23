from odoo import models
import requests
from datetime import datetime, date


class CronJob(models.AbstractModel):
    _name = 'school_management.cron.job'

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
                    today = datetime.today().date()
                    today_attendance = self.env['school_management.attendance'].search_count(
                        [('user', '=', student.id), ('effective_date', '>=', today), ('effective_date', '<=', today)])
                    if today_attendance:
                        continue

                    self.env['school_management.attendance'].create({
                        'user': student.id,
                        'present': True,
                        'access_id': log['access_id']
                    })
                    if student.guardian:
                        sms_config = self.env['sm.sms.config'].search([], limit=1)
                        if sms_config.sms_on_present:
                            sms_content = sms_config.sms_on_present
                            message = sms_content.replace("{student_name}", student.name)
                            response = self.env['school_management.helper'].send_normal_sms(student.guardian.phone,
                                                                                            message)
                            print(response.text)

    def process_absent(self):
        self.env['school_management.helper'].send_normal_sms("01673050495", "Process Absent")
