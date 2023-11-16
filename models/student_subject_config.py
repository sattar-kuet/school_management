from odoo import fields, models, api
from datetime import datetime


class StudentSubjectConfig(models.Model):
    _name = 'sm.student.subject.config'
    _description = 'Student Subject Config'

    student = fields.Many2one('res.users', string='Student')
    available_main_subjects = fields.Many2many('school_management.subject', compute='_compute_available_main_subjects')
    main_subject = fields.Many2one('school_management.subject', string='Main Subjects',
                                   domain="[('id', 'in', available_main_subjects)]")
    available_optional_subjects = fields.Many2many('school_management.subject',
                                                   compute='_compute_available_optional_subjects')
    optional_subject = fields.Many2one('school_management.subject', string='Optional Subjects',
                                       domain="[('id', 'in', available_optional_subjects)]")

    @api.depends('student')
    def _compute_available_main_subjects(self):
        for record in self:
            subject_ids = []
            if record.student.class_config.has_group:
                for setup_line in record.student.class_config.setup_lines:
                    if not setup_line.subject.mandatory and record.student.student_group.id in setup_line.subject.groups.ids:

                        print('*' * 100, setup_line.subject.groups.ids)
                        print('>' * 100, record.student.student_group.id)
                        subject_ids.append(setup_line.subject.id)

            record.available_main_subjects = subject_ids

    @api.depends('main_subject')
    def _compute_available_optional_subjects(self):
        for record in self:
            available_main_subjects = record.available_main_subjects.ids
            if record.main_subject.id in available_main_subjects:
                available_main_subjects.remove(record.main_subject.id)

            record.available_optional_subjects = available_main_subjects

    @api.onchange('main_subject')
    def onchange_main_subject(self):
        for record in self:
            record.optional_subject = False
