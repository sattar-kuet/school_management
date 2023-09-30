# -*- coding: utf-8 -*-

from odoo import fields, models,api


class Result(models.Model):
    _name = 'school_management.result'
    _description = 'Result Management'

    exam = fields.Many2one('school_management.exam', string='Exam', required=True)
    class_name = fields.Char(compute='_compute_class_name')
    student = fields.Many2one('res.users', string="Student", required=True)
    subject = fields.Many2one('school_management.subject', string='Subject')
    written_mark = fields.Float(string='Written Mark')
    mcq_mark = fields.Float(string='MCQ Mark')
    practical_mark = fields.Float(string='Practical Mark')
    status = fields.Selection([('pending', 'Pending'), ('done', 'Done')], default='pending')

    @api.model
    def _compute_class_name(self):
        for record in self:
            record.class_name = record.exam.class_config.name
