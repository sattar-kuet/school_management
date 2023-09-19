# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api


class ClassConfig(models.Model):
    _name = 'school_management.class_config'
    _description = 'School Management'

    name = fields.Char(string='Name', required=True, translate=True)