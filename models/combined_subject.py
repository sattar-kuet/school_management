# -*- coding: utf-8 -*-

from odoo import fields, models, api


class CombinedSubject(models.Model):
    _name = 'school_management.combined_subject'
    _description = 'Subject Management'
    _rec_name = 'title'

    title = fields.Char(string='Name', required=True)
    subject = fields.Many2many('school_management.subject', relation='school_management_subject_title_subjects_rel')
    has_practical = fields.Boolean(string='Has Practical')
    has_mcq = fields.Boolean(string='Has MCQ')
    has_written = fields.Boolean(string='Has Written')
    groups = fields.Many2many('school_management.group')
