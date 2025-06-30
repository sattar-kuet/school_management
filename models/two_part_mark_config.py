# -*- coding: utf-8 -*-

from odoo import fields, models


class TwoPartMarkConfig(models.Model):
    _name = 'sm.two.part.mark.config'
    _description = 'Two Part Mark Config'

    exam = fields.Many2one('school_management.exam', string='Exam')
    subject = fields.Many2one('sm.subject', string='Subject')
    written_max_mark = fields.Float(string='Written Max Marks')
    mcq_max_mark = fields.Float(string='MCQ Max Marks')
    practical_max_mark = fields.Float(string='Practical Max Marks')
