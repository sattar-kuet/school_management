# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProcessedResult(models.Model):
    _name = 'school_management.processed_result'
    _description = 'Processed Result'

    exam = fields.Many2one('school_management.exam', string='Exam', required=True,)
    student = fields.Many2one('res.users', string='Student')
    subject = fields.Many2one('school_management.subject', string='Subject')
    grade_point = fields.Float(string='Grade Point')
    total_mark = fields.Float(string='Total Mark')
    grade_title = fields.Char(string='Grade Title')
