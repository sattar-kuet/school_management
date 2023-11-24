# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api
from odoo.exceptions import ValidationError


class Exam(models.Model):
    _name = 'school_management.exam'
    _description = 'Exam'
    _rec_name = 'title_with_class_date'

    title_with_class_date = fields.Char(string='Name', compute='_compute_title_with_class_date')
    name = fields.Char(string='Name', required=True)
    class_config = fields.Many2one('sm.class_config')
    status = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('setup_done', 'Setup Done'),
            ('processing', 'Processing'),
            ('published', 'Result Published'),
            ('archive', 'Archive')
        ],
        string='Status',
        default='pending'
    )
    ready_to_publish = fields.Boolean(compute='_compute_ready_to_publish', default=False)

    def _compute_title_with_class_date(self):
        for exam in self:
            exam_create_date = self.env['school_management.helper'].formatted_date(exam.create_date)
            exam.title_with_class_date = f'{exam.name} - {exam.class_config.name} - {exam_create_date}'

    def _compute_ready_to_publish(self):
        for record in self:
            if record.status == 'processing' and self.env['school_management.result'].search_count(
                    [('exam', '=', record.id), ('status', '=', 'pending')]):
                record.ready_to_publish = False
            else:
                record.ready_to_publish = True

    @api.model
    def create(self, vals):
        students = self.env['res.users'].search_count([('class_config', '=', vals['class_config'])])

        if students == 0:
            raise ValidationError('There is no student for this Class')
            return
        self.archive_old(vals['class_config'])
        return super(Exam, self).create(vals)

    def processing(self):
        if self.env['school_management.exam'].search_count([('class_config', '=', self.class_config.id),
                                                            ('status', '=', 'processing')]) > 0:
            raise ValidationError('There is another Exam of this class is being processed')
            return
        # self.archive_old(self.class_config.id)
        exam = self
        # ****************************************  ATTENTION  *****************************************
        #  Archive all record which are already published and duplicate current exam to create new one
        # **********************************************************************************************
        if self.status == 'published':
            # *************************  Archive already published Record **********************************
            self.status == 'archive'
            results = self.env['school_management.result'].search([('exam', '=', self.id)])
            for result in results:
                result.status = 'archive'

            processed_results = self.env['school_management.processed_result'].search([('exam', '=', self.id)])
            for processed_result in processed_results:
                processed_result.status = 'archive'

            processed_final_results = self.env['school_management.processed_final_result'].search(
                [('exam', '=', self.id)])
            for processed_final_result in processed_final_results:
                processed_final_result.status = 'archive'

            # *******************  Auto Create new Exam with same detail of previous Exam ****************
            exam = self.env['school_management.exam'].create({
                'name': self.name,
                'class_config': self.class_config.id,
                'status': 'processing'
            })
            result_configs = self.env['school_management.result_config'].search([('exam', '=', self.id)])
            for result_config in result_configs:
                result_config.write({'exam': [(4, exam.id)]})
            two_part_mark_configs = self.env['sm.two.part.mark.config'].search([('exam', '=', self.id)])
            for two_part_mark_config in two_part_mark_configs:
                self.env['sm.two.part.mark.config'].create({
                    'exam': exam.id,
                    'subject': two_part_mark_config.subject.id,
                    'written_max_mark': two_part_mark_config.written_max_mark,
                    'mcq_max_mark': two_part_mark_config.mcq_max_mark,
                    'practical_max_mark': two_part_mark_config.practical_max_mark
                })

        students = self.env['res.users'].search([('class_config', '=', exam.class_config.id)])

        for setup_line in exam.class_config.setup_lines:
            for student in students:
                self.env['school_management.result'].create({
                    'subject': setup_line.subject.id,
                    'exam': exam.id,
                    'student': student.id
                })

        exam.status = 'processing'

    def archive_old(self, class_config_id):

        old_exams = self.env['school_management.exam'].search([('class_config', '=', class_config_id)])
        for old_exam in old_exams:
            old_exam.sudo().status = 'archive'

        old_processed_results = self.env['school_management.processed_result'].search(
            [('class_config', '=', class_config_id)])
        for old_processed_result in old_processed_results:
            old_processed_result.status = 'archive'

    def result_publishing(self):
        self.status = 'published'
        result_configs = self.env['school_management.result_config'].search([('exam', '=', self.id)])
        # process this result_configs.subject for all student
        for result_config in result_configs:
            subject_ids = result_config.subject.subject.ids
            results = self.env['school_management.result'].search([
                ('exam', '=', self.id),
                ('subject', 'in', subject_ids),
            ])

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

            total_max_mark = result_config.written_max_mark_computed + result_config.mcq_max_mark_computed + result_config.practical_max_mark_computed

            for student_id in students_processed:
                if total_max_mark == 0:
                    marks_in_percentage = 0
                else:
                    marks_in_percentage = (total_marks[student_id] / total_max_mark) * 100

                if written_marks[student_id] < result_config.written_pass_mark \
                        or mcq_marks[student_id] < result_config.mcq_pass_mark or \
                        practical_marks[student_id] < result_config.practical_pass_mark:
                    grade_point = 0
                    grade = 'F'
                else:
                    grade_config = self.env['school_management.grade_config'].search(
                        [('min_mark', '<=', marks_in_percentage), ('max_mark', '>=', marks_in_percentage)])

                    grade = grade_config.name
                    grade_point = grade_config.point

                result_data = {
                    'exam': self.id,
                    'class_config': self.class_config.id,
                    'student': student_id,
                    'subject': result_config.subject.id,
                    'grade_point': grade_point,
                    'total_marks': total_marks[student_id],
                    'marks_in_percentage': marks_in_percentage,
                    'grade_title': grade,
                }

                self.env['school_management.processed_result'].create(result_data)
        self.process_final_result()

    def process_final_result(self):
        subject_ids = []
        for setup_line in self.class_config.setup_lines:
            subject_ids.append(setup_line.subject.id)

        total_subject = self.env['school_management.combined_subject'].search_count([('subject', 'in', subject_ids)])
        processed_results = self.env['school_management.processed_result'].search([('exam', '=', self.id)])

        processed_students = []
        total_grade_point = {}
        total_marks = {}
        failed_students = []
        for processed_result in processed_results:
            if processed_result.student.id in failed_students:
                total_marks[processed_result.student.id] += processed_result.total_marks
                continue

            if processed_result.grade_point == 0:
                total_grade_point[processed_result.student.id] = 0
                total_marks[processed_result.student.id] = processed_result.total_marks
                failed_students.append(processed_result.student.id)
                processed_students.append(processed_result.student.id)
                continue

            if processed_result.student.id in processed_students:
                total_grade_point[processed_result.student.id] += processed_result.grade_point
                total_marks[processed_result.student.id] += processed_result.total_marks
            else:
                total_grade_point[processed_result.student.id] = processed_result.grade_point
                total_marks[processed_result.student.id] = processed_result.total_marks
                processed_students.append(processed_result.student.id)
        # print('>'*100)
        # print(total_marks)
        for processed_student_id in processed_students:
            grade_point = total_grade_point[processed_student_id] / total_subject
            grade_config = self.env['school_management.grade_config'].search(
                [('point', '<=', grade_point)], order='point DESC', limit=1)
            final_result = self.env['school_management.processed_final_result'].create({
                'exam': self.id,
                'class_config': self.class_config.id,
                'student': processed_student_id,
                'grade_point': grade_point,
                'grade_title': grade_config.name,
                'total_marks': total_marks[processed_student_id]
            })
            student = self.env['res.users'].browse(processed_student_id)
            sms_config = self.env['sm.sms.config'].browse(1)
            if sms_config.sms_on_result_publish:
                sms_content = sms_config.sms_on_result_publish
                sms_content = sms_content.replace("{exam_title}", str(self.name))
                sms_content = sms_content.replace("{student_name}", str(student.name))
                sms_content = sms_content.replace("{total_mark}", str(final_result.total_marks))
                sms_content = sms_content.replace("{grade_title}", str(final_result.grade_title))
                sms_content = sms_content.replace("{grade_point}", str(final_result.grade_point))
                self.env['school_management.helper'].send_normal_sms(student.guardian.phone, sms_content)

    def remove_setup(self):
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
