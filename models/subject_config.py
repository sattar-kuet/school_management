# -*- coding: utf-8 -*-

from odoo import fields, models


class SubjectConfig(models.Model):
    _name = 'school_management.subject_config'
    _description = 'Subject Management'

    class_config = fields.Many2one("school_management.class_config", string='Class Config', required=True)
    subject = fields.Many2many("school_management.subject", string='Subject')
