# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.odoo import api


class Exam(models.Model):
    _name = 'sm.exams'
    _description = 'School Management'

    name = fields.Char(string='Name', required=True, translate=True)
    session_start = fields.Char(string='Session Start', required=True)
    session_end = fields.Char(string='Session End', compute='_compute_session_end', store=True, default='Null')

    @api.depends('session_start')
    def _compute_session_end(self):
        record = []
        for record in self:
            start_year = int(record.session_start)
            end_year = start_year + 1
            record.session_end = str(end_year)