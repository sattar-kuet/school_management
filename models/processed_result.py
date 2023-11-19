# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProcessedResult(models.Model):
    _name = 'school_management.processed_result'
    _description = 'Processed Result'

    exam = fields.Many2one('school_management.exam', string='Exam', required=True, )
    class_config = fields.Many2one('sm.class_config')
    student = fields.Many2one('res.users', string='Student', domain=lambda self: [
            ("groups_id", "in", [self.env.ref("school_management.group_school_student").id])])
    subject = fields.Many2one('school_management.combined_subject', string='Subject')
    grade_point = fields.Float(string='Grade Point')
    total_marks = fields.Float(string='Total Mark')
    marks_in_percentage = fields.Float(string='Mark (%)')
    grade_title = fields.Char(string='Grade Title')
    status = fields.Selection([('published', 'Published'), ('archive', 'Archive')], default='published')



