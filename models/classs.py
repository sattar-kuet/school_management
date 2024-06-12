# -*- coding: utf-8 -*-
from odoo import fields, models
from datetime import datetime


class Classs(models.Model):
    _name = 'sm.class'
    _description = 'School Management'

    name = fields.Char(string='Name', required=True)
    



