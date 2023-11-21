# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api
import random


class User(models.Model):
    _inherit = 'res.users'
    _description = 'School Management User'
    _rec_name = 'computed_name'

    computed_name = fields.Char(compute='_computed_name')
    code = fields.Char(string='Code')
    attendance_device_user_id = fields.Char()
    roll = fields.Char(string="Roll")
    blood_group = fields.Selection([
        ('a+', 'A+'),
        ('b+', 'B+'),
        ('ab+', 'AB+'),
    ], string='Blood Group')
    guardian = fields.Many2one("res.users", string="Guardian", domain=lambda self: [
            ("groups_id", "in", [self.env.ref("school_management.group_school_guardian").id])])
    class_config = fields.Many2one("sm.class_config", string='Class')
    class_has_group = fields.Boolean(compute='_compute_class_has_group')
    student_group = fields.Many2one("school_management.group", string='Group')
    subjects = fields.Many2many("school_management.subject", string='Subjects')
    designation = fields.Many2one("sm.designation", string="Designation")

    _sql_constraints = [
        ('attendance_device_user_id_unique',
         'UNIQUE(attendance_device_user_id)',
         'Attendance Device User ID must be unique!')
    ]

    def _computed_name(self):
        for record in self:
            if record.class_config:
                record.computed_name = f'{record.name} - {record.class_config.name} - {record.roll}'
            else:
                record.computed_name = f'{record.name} - {record.phone}'

    @api.depends('class_config')
    def _compute_class_has_group(self):
        for student in self:
            student.class_has_group = student.class_config.has_group
            if not student.class_has_group:
                student.student_group = False

    @api.model
    def create(self, vals):
        code = random.randint(100000, 999999)
        vals['login'] = code
        vals['code'] = code
        created_user = super(User, self).create(vals)
        return created_user
