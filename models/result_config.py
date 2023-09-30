# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResultConfig(models.Model):
    _name = 'school_management.result_config'
    _description = 'Result Config'

    subject = fields.Many2one('school_management.combined_subject', string='Subject', required=True, relation='subject_combined_subject')
    exam = fields.Many2many('school_management.exam', string='Exam')
    exam_computed = fields.Char(compute='_exam_computed')
    written_pass_mark = fields.Float(string='Written Pass Mark')
    written_max_mark = fields.Float(string='Written Max Mark')
    mcq_pass_mark = fields.Float(string='MCQ Pass Mark')
    mcq_max_mark = fields.Float(string='MCQ Max Mark')
    practical_pass_mark = fields.Float(string='Practical Pass Mark')
    practical_max_mark = fields.Float(string='Practical Max Mark')

    has_practical = fields.Boolean(compute="_has_practical")
    has_mcq = fields.Boolean(compute="_has_mcq")
    has_written = fields.Boolean(compute="_has_written")
    status = fields.Selection([('generated', 'System Generated'), ('configured', 'Configured')], defualt='generated')

    def _exam_computed(self):
        for record in self:
            if record.exam:
                record.exam_computed = record.exam.name
            else:
                record.exam_computed = 'ALL'

    @api.depends('subject.has_practical')
    def _has_practical(self):
        for record in self:
            record.has_practical = record.subject.has_practical

    @api.depends('subject.has_mcq')
    def _has_mcq(self):
        for record in self:
            record.has_mcq = record.subject.has_mcq

    @api.depends('subject.has_written')
    def _has_written(self):
        for record in self:
            record.has_written = record.subject.has_written


