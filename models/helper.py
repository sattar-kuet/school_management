from odoo import models
import requests


class Helper(models.AbstractModel):
    _name = 'school_management.helper'

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
