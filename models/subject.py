# -*- coding: utf-8 -*-

from odoo import fields, models


class Subject(models.Model):
    _name = 'school_management.subject'
    _description = 'Subject Management'

    name = fields.Char(string='Name', required=True, translate=True)
    has_practical = fields.Boolean(string='Has Practical', translate=True)
    has_mcq = fields.Boolean(string='Has MCQ', translate=True)
    has_written = fields.Boolean(string='Has Written', translate=True)
    has_two_part = fields.Char(string='Has two Part',compute='pass')