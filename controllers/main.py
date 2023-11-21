from odoo import http
from odoo.http import request
import json


class SchoolManagement(http.Controller):
    @http.route('/school_management/test', type="http", auth="public", methods=["GET"])
    def test(self):
        request.env['school_management.helper'].pull_attendance_record()
        return 'OK testing.'

    @http.route('/school_management/result_config', type="json", auth="public", methods=['POST'])
    def result_config(self, **data):
        received_data = http.request.httprequest.data
        received_data_str = received_data.decode('utf-8')
        received_data = json.loads(received_data_str)
        print('*' * 100, received_data)
        result_config = request.env['sm.two.part.mark.config'].sudo().search([
            ('exam', '=', received_data['exam_id']),
            ('subject', '=', received_data['subject_id'])
        ])

        if result_config:
            return {
                'written_max_mark': result_config.written_max_mark,
                'mcq_max_mark': result_config.mcq_max_mark,
                'practical_max_mark': result_config.practical_max_mark,
            }
        combined_subject = request.env['school_management.combined_subject'].search(
            [('subject', '=', received_data['subject_id'])], limit=1)
        result_config = request.env['school_management.result_config'].search([
            ('exam', '=', received_data['exam_id']),
            ('subject', '=', combined_subject.id),
        ], limit=1)
        return {
            'written_max_mark': result_config.written_max_mark,
            'mcq_max_mark': result_config.mcq_max_mark,
            'practical_max_mark': result_config.practical_max_mark,
        }
