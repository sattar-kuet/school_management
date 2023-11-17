# -*- coding: utf-8 -*-

from odoo import fields, models

class Designation(models.Model):
    _name = 'sm.designation'
    _description = 'Designation'

    name = fields.Char(string='Name')