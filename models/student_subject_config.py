from odoo import fields, models, api
from datetime import datetime


class StudentSubjectConfig(models.Model):
    _name = 'sm.student.subject.config'
    _description = 'Student Subject Config'

    student = fields.Many2one('res.users', string='Student')
    available_main_subjects = fields.Many2many('school_management.subject', compute='_compute_available_main_subjects')
    main_subject = fields.Many2one('school_management.subject', string='Main Subjects',
                                   domain="[('id', 'in', available_main_subjects)]")
    optional_subject = fields.Many2one('school_management.subject', string='Optional Subjects')

    @api.depends('student')
    def _compute_available_main_subjects(self):
        for record in self:
            subject_ids = []
            if record.student.class_has_group:
                for setup_line in record.student.class_config.setup_lines:
                    if not setup_line.subject.mandatory:
                        subject_ids.append(setup_line.subject.id)
            record.available_main_subjects = subject_ids

    @api.onchange('main_subject')
    def onchange_main_subject(self):
        if self.main_subject:
            return {'domain': {'optional_subject': [('id', '!=', self.main_subject.id)]}}
        else:
            return {'domain': {'optional_subject': []}}
