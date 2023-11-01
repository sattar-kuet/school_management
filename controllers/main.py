from odoo import http
from odoo.http import request
import json


class SchoolManagement(http.Controller):

    @http.route('/search_result/<string:student_code>', type="http", auth="public", website=True,
                methods=['GET', 'POST'])
    def search_result(self, student_code, **kw):
        student = request.env['res.users'].search([('code', '=', student_code)])
        result = request.env['school_management.processed_final_result'].search(
            [('student', '=', student_code), ('status', '=', 'published')])
        response = {'name': student.name, 'grade_point': result.grade_point, 'grade_title': result.grade_title}
        return json.dumps(response)

    @http.route('/dashboard', type="http", auth="user", website=True, methods=['GET', 'POST'])
    def portal_home(self, **kw):
        exam = request.env['school_management.exam'].search([('status', '=', 'processing')], limit=1)
        if not exam:
            return request.render('school_management.portal_layout', {'no_active_exam': True})
        data = []
        processed_students = request.env['school_management.processed_result'].se
        for class_record in exam.classes:
            student = request.env['res.users'].search([
                ('class_config', '=', class_record.id),
                ('id', 'not in', processed_students)
            ])
            subject_config = request.env['school_management.subject_config'].search(
                [('class_config', '=', class_record.id)])

            for student in students:
                data.append({
                    'student': student,
                    'subjects': subject_config.subject
                })

        final_data = {
            'exam': exam,
            'data_list': data,
            'debug': subject_config.subject
        }
        values = {'data': final_data, 'no_active_exam': False, 'page': 'dashboard'}
        return request.render('school_management.portal_layout', values)


