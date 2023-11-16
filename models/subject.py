# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Subject(models.Model):
    _name = 'school_management.subject'
    _description = 'Subject Management'

    name = fields.Char(string='Name', required=True)
    has_practical = fields.Boolean(string='Has Practical')
    has_mcq = fields.Boolean(string='Has MCQ')
    has_written = fields.Boolean(string='Has Written')
    groups = fields.Many2many('school_management.group')
    mandatory = fields.Boolean(default=True)

    def write(self, vals):
        combined_subject = self.env['school_management.combined_subject'].search([('subject', 'in', self.ids)], limit=1)
        print('*'*100,combined_subject)
        print('*'*100,vals)
        if combined_subject:
            if 'has_practical' in vals:
                combined_subject.has_practical = vals['has_practical']
            elif 'has_mcq' in vals:
                combined_subject.has_mcq = vals['has_mcq']
            elif 'has_written' in vals:
                combined_subject.has_written = vals['has_written']
            elif 'groups' in vals:
                combined_subject.groups = vals['groups']
            elif 'mandatory' in vals:
                combined_subject.mandatory = vals['mandatory']
        return super(Subject, self).write(vals)
