# -*- coding: utf-8 -*-

from odoo import fields, models


class StudentPromotionConfig(models.Model):
    _name = 'sm.student.promotion.config'
    _description = 'Student Promotion Config'

    type = fields.Selection([('auto_x', 'Auto in all Class'),
                             ('auto_p', 'Auto if Pass'),
                             ('manual', 'Manual')], string='Title', required=True)