# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api


class Exam(models.Model):
    _name = 'school_management.exam'
    _description = 'Exam'

    name = fields.Char(string='Name', required=True, translate=True)
    status = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('taken', 'Taken')
        ],
        string='Status',
        default='pending'
    )