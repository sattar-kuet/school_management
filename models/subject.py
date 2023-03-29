# -*- coding: utf-8 -*-

from odoo import fields, models


class Subject(models.Model):
    _name = 'sm.subjects'
    _description = 'Subject Management'

    name = fields.Char(string='Name', required=True, translate=True)
    first_paper = fields.Char(string='First Paper', translate=True)
    second_paper = fields.Char(string='Second Paper', translate=True)
    first_paper_practical = fields.Char(string='First Paper Practical', translate=True)
    second_paper_practical = fields.Char(string='Second Paper Practical', translate=True)
    group = fields.Selection([
        ('all_group', 'All Group'),
        ('science', 'Science'),
        ('business_studies', 'Business Studies'),
        ('humanities', 'Humanities'),
    ], string='Group', required=True, translate=True,  default='all_group')
    has_two_part = fields.Boolean(string='Has Two Part')
    has_practical = fields.Boolean(string='Has Practical')
    mandatory = fields.Boolean(string='Mandatory')

