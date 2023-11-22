# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Batch(models.Model):
    _name = 'school_management.batch'
    _description = 'Batch'

    name = fields.Char(string='Name', required=True)
    start_time = fields.Char(string="Start Time")
    end_time = fields.Char(string="End Time")
    students = fields.Many2many('res.users', string="Students", domain=lambda self: [
            ("groups_id", "in", [self.env.ref("school_management.group_school_student").id])])



