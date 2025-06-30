# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Result(models.Model):
    _name = 'school_management.result'
    _description = 'Result Management'

    exam = fields.Many2one('school_management.exam', string='Exam', required=True)
    class_config = fields.Many2one('sm.class_config', compute='_compute_class_config', store=True)
    class_name = fields.Char(compute='_compute_class_name')
    student = fields.Many2one('res.users', string="Student", domain=lambda self: [
            ("groups_id", "in", [self.env.ref("school_management.group_school_student").id])],required=True)
    subject = fields.Many2one('sm.subject', string='Subject')
    written_mark = fields.Float(string='Written Mark')
    mcq_mark = fields.Float(string='MCQ Mark')
    practical_mark = fields.Float(string='Practical Mark')
    status = fields.Selection([('pending', 'Pending'), ('done', 'Done'), ('archive', 'archive')], default='pending')
    written_mark_not_applicable = fields.Boolean(compute='_compute_written_mark_not_applicable')
    mcq_mark_not_applicable = fields.Boolean(compute='_compute_mcq_mark_not_applicable')
    practical_mark_not_applicable = fields.Boolean(compute='_compute_practical_mark_not_applicable')
    save_button_not_applicable = fields.Boolean(compute='_compute_save_button_not_applicable')

    @api.depends('written_mark', 'mcq_mark', 'practical_mark', 'status', 'exam', 'subject')
    def _compute_save_button_not_applicable(self):
        for record in self:
            result_config = self.env['school_management.result_config'].search([
                ('exam', '=', record.exam.id),
                ('subject', '=', record.subject.id)
            ], limit=1)

            record.save_button_not_applicable = False

            if record.status == 'done':
                record.save_button_not_applicable = True

            if result_config:
                if (
                        record.written_mark > result_config.written_max_mark or
                        record.mcq_mark > result_config.mcq_max_mark or
                        record.practical_mark > result_config.practical_max_mark
                ):
                    record.save_button_not_applicable = True

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
        result_config = self.env['school_management.result_config'].search([
            ('exam', '=', self.exam.id),
            ('subject', '=', self.subject.id)
        ], limit=1)

        if 'written_mark' in vals:
            if float(vals['written_mark']) > result_config.written_max_mark:
                vals['status'] = 'pending'
        elif 'mcq_mark' in vals:
            if float(vals['mcq_mark']) > result_config.mcq_max_mark:
                vals['status'] = 'pending'
        elif 'practical_mark' in vals:
            if float(vals['practical_mark']) > result_config.practical_max_mark:
                vals['status'] = 'pending'
        return super(Result, self).write(vals)

    def save(self):
        self.status = 'done'
