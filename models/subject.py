# -*- coding: utf-8 -*-

from odoo import fields, models


class Subject(models.Model):
    _name = 'school_management.subject'
    _description = 'Subject Management'

    name = fields.Char(string='Name', required=True)
    has_practical = fields.Boolean(string='Has Practical')
    has_mcq = fields.Boolean(string='Has MCQ')
    has_written = fields.Boolean(string='Has Written')