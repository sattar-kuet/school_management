# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime


class TeacherActivity(models.Model):
    _name = 'sm.subject.teacher'
    _description = 'Teacher Activity'

    teacher = fields.Many2one('res.users', string='Teacher')
    subject = fields.Many2one('sm.subject', string='Subject')
    class_config = fields.Many2many('sm.class_config', string='Class Config')
