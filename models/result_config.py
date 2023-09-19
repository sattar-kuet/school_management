# -*- coding: utf-8 -*-

from odoo import fields, models


class ResultConfig(models.Model):
    _name = 'school_management.result_config'
    _description = 'Result Config'

    subject = fields.Many2one( 'school_management.subject',string='Subject', required=True, translate=True)
    written_pass_mark = fields.Float(string='Written Pass Mark')
    written_max_mark = fields.Float(string='Written Max Mark')
    mcq_pass_mark = fields.Float(string='MCQ Pass Mark')
    mcq_max_mark = fields.Float(string='MCQ Max Mark')
    practical_pass_mark = fields.Float(string='Practical Pass Mark')
    practical_max_mark = fields.Float(string='Practical Max Mark')
