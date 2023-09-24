# -*- coding: utf-8 -*-

from odoo import fields, models


class Result(models.Model):
    _name = 'school_management.result'
    _description = 'Result Management'

    exam = fields.Many2one('school_management.exam', string='Exam', required=True)
    student = fields.Many2one('res.user')
    subject = fields.Many2one('school_management.subject', string='Subject')
    written_mark = fields.Char(string='Written Mark', required=True)
    mcq_mark = fields.Char(string='MCQ Mark', required=True)
    practical_mark = fields.Char(string='Practical Mark', required=True)

