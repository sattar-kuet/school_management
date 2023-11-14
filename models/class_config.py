# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api


class ClassConfig(models.Model):
    _name = 'school_management.class_config'
    _description = 'School Management'

    name = fields.Char(string='Name', required=True)
    has_group = fields.Boolean(string='Has Group', required=True)
    subjects = fields.Many2many('school_management.subject')

    def _compute_subjects(self):
        for record in self:
            class_subject_config = self.env['school_management.subject_config'].search(
                [('class_config', '=', record.id)], limit=1)
            record.subjects = class_subject_config.subject.ids
