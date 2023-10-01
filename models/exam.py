# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api
from odoo.exceptions import ValidationError


class Exam(models.Model):
    _name = 'school_management.exam'
    _description = 'Exam'

    name = fields.Char(string='Name', required=True)
    class_config = fields.Many2one('school_management.class_config')
    status = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('setup_done', 'Setup Done'),
            ('processing', 'Processing'),
            ('result_published', 'Result Published')
        ],
        string='Status',
        default='pending'
    )

    def processing(self):
        students = self.env['res.users'].search([('class_config', '=', self.class_config.id)])
        subject_config = self.env['school_management.subject_config'].search(
            [('class_config', '=', self.class_config.id)])

        for subject in subject_config.subject:
            for student in students:
                self.env['school_management.result'].create({
                    'subject': subject.id,
                    'exam': self.id,
                    'student': student.id
                })

        self.status = 'processing'

    def result_publishing(self):
        self.status = 'result_published'
        result_configs = self.env['school_management.result_config'].search([('exam', '=', self.id)])
        # process this result_configs.subject for all student
        for result_config in result_configs:
            subject_ids = result_config.subject.subject.ids
            results = self.env['school_management.result'].search([('subject', 'in', subject_ids)])

            written_marks = {}
            mcq_marks = {}
            practical_marks = {}
            total_marks = {}
            students_processed = []
            for result in results:
                if result.student.id in students_processed:
                    written_marks[result.student.id] += result.written_mark
                    mcq_marks[result.student.id] += result.mcq_mark
                    practical_marks[result.student.id] += result.practical_mark
                    total_marks[result.student.id] += result.written_mark + result.mcq_mark + result.practical_mark
                else:
                    written_marks[result.student.id] = result.written_mark
                    mcq_marks[result.student.id] = result.mcq_mark
                    practical_marks[result.student.id] = result.practical_mark
                    total_marks[result.student.id] = result.written_mark + result.mcq_mark + result.practical_mark
                    students_processed.append(result.student.id)
            total_max_mark = result_config.written_max_mark + result_config.mcq_max_mark + result_config.practical_max_mark
            for student_id in students_processed:
                marks_in_percentage = (total_marks[student_id] / total_max_mark) * 100
                if written_marks[student_id] < result_config.written_pass_mark \
                        or mcq_marks[student_id] < result_config.mcq_pass_mark or \
                        practical_marks[student_id] < result_config.practical_pass_mark:
                    grade_point = 0
                    grade = 'F'
                else:
                    grade_config = self.env['school_management.grade_config'].search(
                        [('min_mark', '<=', marks_in_percentage), ('max_mark', '>=', marks_in_percentage)])

                    print("grade_config")
                    print(grade_config)
                    print(marks_in_percentage)
                    grade = grade_config.name
                    grade_point = grade_config.point

                result_data = {
                    'exam': self.id,
                    'student': student_id,
                    'subject': result_config.subject.id,
                    'grade_point': grade_point,
                    'total_marks': total_marks[student_id],
                    'marks_in_percentage': marks_in_percentage,
                    'grade_title': grade,
                }
                print('data >>>>>>>>>>>>>>')
                print(result_data)

                self.env['school_management.processed_result'].create(result_data)

    def remove_setup(self):
        print('here..')
        print(self.id)
        result_config = self.env['school_management.result_config'].search([('exam', '=', self.id)], limit=1)
        if len(result_config.exam.ids) == 1:
            raise ValidationError(
                'This exam setup is not coupled with any others settings. So you just need to modify it.')
        else:
            result_configs = self.env['school_management.result_config'].search([('exam', '=', self.id)])
            for result_config in result_configs:
                new_exam_ids = [x for x in result_config.exam.ids if x != self.id]
                result_config.write({
                    'exam': new_exam_ids
                })
        self.status = 'pending'
