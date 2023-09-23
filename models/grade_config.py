# -*- coding: utf-8 -*-

from odoo import fields, models


class GradeConfig(models.Model):
    _name = 'school_management.grade_config'
    _description = 'School Management'

    name = fields.Char(string='Name', required=True)
    min_mark = fields.Float(string='Min Mark', required=True)
    max_mark = fields.Float(string='Max Mark', required=True)
    point = fields.Float(string='Point', required=True)