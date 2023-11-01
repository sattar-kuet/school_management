from odoo import fields, models, api
from datetime import datetime


class StudentSubjectConfig(models.Model):
    _name = 'sm.student.subject.config'
    _description = 'Student Subject Config'

    student = fields.Many2one('res.users', string='Student')
    subjects = fields.Many2one('school_management.subject', string='Subjects')
    optional_subject = fields.Char(string='Optional Subject')
