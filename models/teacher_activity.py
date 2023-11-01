# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime


class TeacherActivity(models.Model):
    _name = 'sm.teacher.activity'
    _description = 'Teacher Activity'

    teacher = fields.Many2one('res.users', string='Teacher')
    subject = fields.Many2one('school_management.subject', string='Subject')
    class_config = fields.Many2many('school_management.class_config', string='Class Config')
