from odoo import models
import requests
from datetime import datetime, date
import pytz


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
        time_zone_obj = pytz.timezone("Asia/Dhaka")
        current_time = datetime.now(time_zone_obj).time()
        current_date = datetime.now(time_zone_obj).date()
        current_day_numeric = current_date.weekday()

        domain = [
            ('start_time', '<=', current_time.strftime('%H:%M')),
            ('end_time', '>=', current_time.strftime('%H:%M'))
        ]
        matching_batches = self.env['school_management.batch'].search(domain)

        print(current_day_numeric)
        for matching_batch in matching_batches:
            off_days_values = matching_batch.mapped('off_days.value')
            if current_day_numeric in off_days_values:
                continue

            start_of_day = time_zone_obj.localize(datetime.combine(current_date, datetime.min.time()))
            end_of_day = time_zone_obj.localize(datetime.combine(current_date, datetime.max.time()))

            domain = [
                ('create_date', '>=', start_of_day.strftime('%Y-%m-%d %H:%M:%S')),
                ('create_date', '<=', end_of_day.strftime('%Y-%m-%d %H:%M:%S')),
            ]
            present_student_ids = self.env['school_management.attendance'].search(domain).mapped('user.ids')
            sms_sent_to_student_ids = self.env['school_management.absent'].search(domain).mapped('user.id')
            for student_id in matching_batch.student.ids:
                if student_id not in present_student_ids and student_id not in sms_sent_to_student_ids:
                    # TODO send sms for this student
                    self.env['school_management.absent'].create({
                        'user': student_id
                    })

