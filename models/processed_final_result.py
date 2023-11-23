# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProcessedFinalResult(models.Model):
    _name = 'school_management.processed_final_result'
    _description = 'Processed Final Result'

    exam = fields.Many2one('school_management.exam', string='Exam', required=True)
    merit_position = fields.Integer('Merit Position')
    class_config = fields.Many2one('sm.class_config')
    student = fields.Many2one('res.users', string='Student', domain=lambda self: [
            ("groups_id", "in", [self.env.ref("school_management.group_school_student").id])])
    grade_point = fields.Float(string='Grade Point', digits=(3, 2))
    total_marks = fields.Float(string='Total Mark',digits=(6, 2))
    marks_in_percentage = fields.Float(string='Mark (%)')
    grade_title = fields.Char(string='Grade Title')
    status = fields.Selection([('published', 'Published'), ('archive', 'Archive')], default='published')



