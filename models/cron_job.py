from odoo import models
import requests
from datetime import datetime, timedelta
import pytz


class CronJob(models.AbstractModel):
    _name = 'school_management.cron.job'

    def pull_attendance_record(self):
        time_zone_obj = pytz.timezone("Asia/Dhaka")
        current_time = datetime.now(time_zone_obj).time()
        domain = [
            ('start_time', '<=', current_time.strftime('%H:%M')),
            ('end_time', '>=', current_time.strftime('%H:%M'))
        ]
        current_batches = self.env['school_management.batch'].search(domain)
        sms_config = self.env['sm.sms.config'].search([], limit=1)
        max_delay_on_absent = sms_config.max_delay_on_absent
        print('*' * 100)
        print('attendance processing')
        for current_batch in current_batches:
            batch_start_time_str = current_batch.start_time
            batch_start_time = datetime.strptime(batch_start_time_str, "%H:%M").time()
            end_time = datetime.combine(datetime.today(), batch_start_time) + timedelta(minutes=max_delay_on_absent)
            end_time = end_time.time()
            print('*' * 100)
            print(end_time)
            if current_time > end_time:
                continue

            largest_access_id = self.env['school_management.attendance'].search([('access_id', '!=', False)],
                                                                                order='access_id desc', limit=1)
            access_id = 27774600
            if largest_access_id:
                access_id = largest_access_id.access_id
            # print("^" * 100)
            # print(access_id)
            end_point = 'https://rumytechnologies.com/rams/json_api'
            current_date = datetime.now(time_zone_obj).now()
            pay_load = {
                "operation": "fetch_log",
                "auth_user": "HTRMathematics",
                "auth_code": "h2q6uzc6s6jkb82pygo4fb5ap4fsqpc",
                "start_date": current_date.strftime("%Y-%m-%d"),
                "end_date": current_date.strftime("%Y-%m-%d"),
                "start_time": "00:00:00",
                "end_time": "23:59:59",
                "access_id": f"{access_id}"
            }
            print(pay_load)
            response = requests.post(end_point, json=pay_load)
            if response.status_code == 200:
                # Assuming the response is JSON
                response_data = response.json()
                print('*' * 100, response_data)
                for log in response_data["log"]:
                    student = self.env['res.users'].search([('attendance_device_user_id', '=', log['registration_id'])],
                                                           limit=1)
                    if student:
                        today = datetime.today().date()
                        today_attendance = self.env['school_management.attendance'].search_count(
                            [('user', '=', student.id), ('effective_date', '>=', today),
                             ('effective_date', '<=', today)])
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

            domain = [('effective_date', '>=', start_of_day.strftime('%Y-%m-%d %H:%M:%S')),
                      ('effective_date', '<=', end_of_day.strftime('%Y-%m-%d %H:%M:%S')),
                      ('present', '=', True)
                      ]
            present_student_ids = self.env['school_management.attendance'].search(domain).mapped('user.id')

            domain = [('effective_date', '>=', start_of_day.strftime('%Y-%m-%d %H:%M:%S')),
                      ('effective_date', '<=', end_of_day.strftime('%Y-%m-%d %H:%M:%S')),
                      ('present', '=', False)
                      ]
            sms_sent_to_student_ids = self.env['school_management.attendance'].search(domain).mapped('user.id')
            print('sms_sent_to_student_ids')
            print(sms_sent_to_student_ids)
            for student_id in matching_batch.students.ids:
                if student_id not in present_student_ids and student_id not in sms_sent_to_student_ids:
                    print('Absent student id')
                    print(student_id)
                    sms_config = self.env['sm.sms.config'].search([], limit=1)
                    if sms_config.sms_on_absent:
                        sms_content = sms_config.sms_on_absent
                        student = self.env['res.users'].browse(student_id)
                        message = sms_content.replace("{student_name}", student.name)
                        response = self.env['school_management.helper'].send_normal_sms(student.guardian.phone,
                                                                                        message)
                        print(response.text)
                    self.env['school_management.attendance'].create({
                        'user': student_id,
                        'present': False
                    })
