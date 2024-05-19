from odoo import models
import requests
import pytz


class Helper(models.AbstractModel):
    _name = 'school_management.helper'

    @staticmethod
    def formatted_date(date_obj):
        bd_tz = pytz.timezone("Asia/Dhaka")
        bd_time = date_obj.astimezone(bd_tz)
        date_format = "%d %b %Y"
        return bd_time.strftime(date_format)

    @staticmethod
    def send_normal_sms(phone, message):
        pay_load = {
            'token': 'OJfnlVSqaAzgg61dQWOH',
            'phone': phone,
            'message': message
        }
        end_point = 'https://client.itscholarbd.com/sendsms';
        response = requests.post(end_point, data=pay_load)
        return response

    @staticmethod
    def send_sms_via_reve_system(phone, message):
        end_point = "http://103.177.125.106:7788/sendtext?" \
                    "apikey=900ac5b3d53ece22&secretkey=b6984493&" \
                    "callerID=HTR Maths&" \
                    f"toUser={phone}&messageContent={message}"

        response = requests.get(end_point)
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
