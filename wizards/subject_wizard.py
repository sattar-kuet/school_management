# -*- coding: utf-8 -*-

from odoo import fields, models


class SubjectWizard(models.TransientModel):
    _name = 'school_management.subject.wizard'
    _description = 'Subject Wizard'

    name = fields.Char(string='Name', required=True)
    part1 = fields.Char(compute="_compute_part1")
    part2 = fields.Char(compute="_compute_part2")
    has_practical = fields.Boolean(string='Has Practical')
    has_mcq = fields.Boolean(string='Has MCQ')
    has_written = fields.Boolean(string='Has Written')
    has_two_part = fields.Char(string='Has two Part', compute='pass')
