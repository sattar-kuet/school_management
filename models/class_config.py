# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api


class ClassConfig(models.Model):
    _name = 'school_management.class_config'
    _description = 'School Management'

    name = fields.Char(string='Name', required=True)
    shift = fields.Many2one('school_management.shift')
    setup_lines = fields.Many2many('school_management.class.setup.line')


class ClassSetupLine(models.Model):
    _name = 'school_management.class.setup.line'
    _description = 'Class Setup line'


