# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProccessedResult(models.Model):
    _name = 'school_management.proccessed_result'
    _description = 'Proccessed Result'

    exam = fields.Many2one('school_management.exam', string='Exam', required=True,)
    student = fields.Many2one('school_management.student', string='Student')
    subject = fields.Many2one('school_management.subject', string='Subject')
    grade_point = fields.Float(string='Grade Point')
    total_mark = fields.Float(string='Total Mark')
    grade_title = fields.Char(string='Grade Title')
