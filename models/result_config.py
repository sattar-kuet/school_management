# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResultConfig(models.Model):
    _name = 'school_management.result_config'
    _description = 'Result Config'

    subject = fields.Many2one('school_management.combined_subject', string='Subject', required=True,
                              relation='subject_combined_subject')
    exam = fields.Many2many('school_management.exam', string='Exam')
    written_pass_mark = fields.Float(string='Written Pass Mark')
    written_max_mark = fields.Float(string='Written Max Mark')
    written_max_mark_computed = fields.Float(string='Written Max Mark', compute='_compute_written_max_mark')
    mcq_pass_mark = fields.Float(string='MCQ Pass Mark')
    mcq_max_mark = fields.Float(string='MCQ Max Mark')
    mcq_max_mark_computed = fields.Float(string='MCQ Max Mark', compute='_compute_mcq_max_mark')
    practical_pass_mark = fields.Float(string='Practical Pass Mark')
    practical_max_mark = fields.Float(string='Practical Max Marks')
    practical_max_mark_computed = fields.Float(string='Practical Max Marks', compute='_compute_practical_max_mark')
    total_pass_mark = fields.Float(string='Total Pass Marks')

    has_practical = fields.Boolean(compute="_has_practical")
    has_mcq = fields.Boolean(compute="_has_mcq")
    has_written = fields.Boolean(compute="_has_written")
    two_part_setup_line = fields.Many2many('sm.two.part.mark.config')
    status = fields.Selection([('generated', 'System Generated'), ('configured', 'Configured')], default='generated')

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

    @api.depends('subject.has_written')
    def _compute_written_max_mark(self):
        for result_config in self:
            result_config.written_max_mark_computed = self.get_written_max_mark(result_config)

    @staticmethod
    def get_written_max_mark(result_config_obj):
        if len(result_config_obj.two_part_setup_line) == 2:
            written_max_mark = 0
            for two_part_setup_line in result_config_obj.two_part_setup_line:
                written_max_mark += two_part_setup_line.written_max_mark
            return written_max_mark
        else:
            return result_config_obj.written_max_mark

    @api.depends('subject.has_mcq')
    def _compute_mcq_max_mark(self):
        for result_config in self:
            result_config.mcq_max_mark_computed = self.get_mcq_max_mark(result_config)

    @staticmethod
    def get_mcq_max_mark(result_config_obj):
        if len(result_config_obj.two_part_setup_line) == 2:
            mcq_max_mark = 0
            for two_part_setup_line in result_config_obj.two_part_setup_line:
                mcq_max_mark += two_part_setup_line.mcq_max_mark
            return mcq_max_mark
        else:
            return result_config_obj.mcq_max_mark

    @api.depends('subject.has_practical')
    def _compute_practical_max_mark(self):
        for result_config in self:
            result_config.practical_max_mark_computed = self.get_practical_max_mark(result_config)

    @staticmethod
    def get_practical_max_mark(result_config_obj):
        if len(result_config_obj.two_part_setup_line) == 2:
            practical_max_mark = 0
            for two_part_setup_line in result_config_obj.two_part_setup_line:
                practical_max_mark += two_part_setup_line.practical_max_mark
            return practical_max_mark
        else:
            return result_config_obj.practical_max_mark

