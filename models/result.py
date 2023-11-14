# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Result(models.Model):
    _name = 'school_management.result'
    _description = 'Result Management'

    exam = fields.Many2one('school_management.exam', string='Exam', required=True)
    class_config = fields.Many2one('sm.class_config', compute='_compute_class_config', store=True)
    class_name = fields.Char(compute='_compute_class_name')
    student = fields.Many2one('res.users', string="Student", required=True)
    subject = fields.Many2one('school_management.subject', string='Subject')
    written_mark = fields.Float(string='Written Mark')
    mcq_mark = fields.Float(string='MCQ Mark')
    practical_mark = fields.Float(string='Practical Mark')
    status = fields.Selection([('pending', 'Pending'), ('done', 'Done'), ('archive', 'archive')], default='pending')
    written_mark_not_applicable = fields.Boolean(compute='_compute_written_mark_not_applicable')
    mcq_mark_not_applicable = fields.Boolean(compute='_compute_mcq_mark_not_applicable')
    practical_mark_not_applicable = fields.Boolean(compute='_compute_practical_mark_not_applicable')

    @api.depends('subject')
    def _compute_written_mark_not_applicable(self):
        for record in self:
            record.written_mark_not_applicable = True
            if record.subject.has_written:
                record.written_mark_not_applicable = False

    @api.depends('subject')
    def _compute_mcq_mark_not_applicable(self):
        for record in self:
            record.mcq_mark_not_applicable = True
            if record.subject.has_mcq:
                record.mcq_mark_not_applicable = False

    @api.depends('subject')
    def _compute_practical_mark_not_applicable(self):
        for record in self:
            record.practical_mark_not_applicable = True
            if record.subject.has_practical:
                record.practical_mark_not_applicable = False

    @api.model
    def _compute_class_name(self):
        for record in self:
            record.class_name = record.exam.class_config.name

    @api.model
    def _compute_class_config(self):
        for record in self:
            record.class_config = record.exam.class_config.id

    def write(self, vals):
        vals['status'] = 'done'
        return super(Result, self).write(vals)
