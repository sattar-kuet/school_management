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
            self.update_subject(combined_subject, vals)
        return super(Subject, self).write(vals)

    @staticmethod
    def update_subject(subject_obj, vals):
        if 'has_practical' in vals:
            subject_obj.has_practical = vals['has_practical']
        elif 'has_mcq' in vals:
            subject_obj.has_mcq = vals['has_mcq']
        elif 'has_written' in vals:
            subject_obj.has_written = vals['has_written']
        elif 'groups' in vals:
            subject_obj.groups = vals['groups']
        elif 'mandatory' in vals:
            subject_obj.mandatory = vals['mandatory']
