# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api
import random


class User(models.Model):
    _inherit = 'res.users'
    _description = 'School Management User'

    code = fields.Char(string='Code')
    roll = fields.Char(string="Roll")
    blood_group = fields.Selection([
        ('a+', 'A+'),
        ('b+', 'B+'),
        ('ab+', 'AB+'),
    ], string='Blood Group', required=True)
    guardian = fields.Many2one("res.users", string="Guardian")
    class_config = fields.Many2one("school_management.class_config", string='Class')
    user_type = fields.Selection([('student', 'Student'), ('teacher', 'Teacher'), ('guardian', 'Guardian')])

    @api.model
    def create(self, vals):
        code = random.randint(100000, 999999)
        vals['login'] = code
        vals['code'] = code

        student_group = self.env['res.groups'].search([
            ('name', '=', 'Student')
        ])
        teacher_group = self.env['res.groups'].search([
            ('name', '=', 'Teacher')
        ])

        if vals:
            if 'is_student' in vals:
                created_user = super(User, self).create(vals)
                created_user.write({
                    'in_group_' + str(student_group.id): True,
                    'in_group_' + str(teacher_group.id): False
                })
            else:
                created_user = super(User, self).create(vals)

            return created_user
