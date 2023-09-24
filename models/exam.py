# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api


class Exam(models.Model):
    _name = 'school_management.exam'
    _description = 'Exam'

    name = fields.Char(string='Name', required=True)
    classes = fields.Many2many('school_management.class_config')
    status = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('taken', 'Taken')
        ],
        string='Status',
        default='pending'
    )

    @api.model
    def create(self, vals):
        return super(Exam, self).create(vals)

    def processing(self):
        print(self.classes)
        for class_record in self.classes:
            students = self.env['school_management.student'].search([('class_config', '=', class_record.id)])
            subject_config = self.env['school_management.subject_config'].search(
                [('class_config', '=', class_record.id)])

            for subject in subject_config.subject:
                for student in students:
                    self.env['school_management.result'].create({
                        'subject': subject.id,
                        'exam': self.id,
                        'student': student.id
                    })

        self.status = 'processing'
