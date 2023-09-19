# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api


class Student(models.Model):
    _name = 'school_management.student'
    _description = 'School Management'

    name = fields.Char(string='Name', required=True, translate=True)
    code = fields.Char(string='Code', compute='pass',store=True)
    roll = fields.Char(string="Roll", required=True, default=False)
    blood_group = fields.Selection([
        ('a+', 'A+'),
        ('b+', 'B+'),
        ('ab+', 'AB+'),
    ], string='Blood Group', required=True, translate=True)
    guardian = fields.Many2one("res.users", string="Guardian")
    class_config = fields.Many2one("school_management.student")

    