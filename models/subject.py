# -*- coding: utf-8 -*-

from odoo import fields, models


class Subject(models.Model):
    _name = 'school_management.subject'
    _description = 'Subject Management'

    name = fields.Char(string='Name', required=True)
    has_practical = fields.Boolean(string='Has Practical')
    has_mcq = fields.Boolean(string='Has MCQ')
    has_written = fields.Boolean(string='Has Written')

    def create(self):
        return {
            'name': 'Add New Subject',
            'view_mode': 'form',
            'res_model': 'school_management.subject.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
