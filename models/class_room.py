# -*- coding: utf-8 -*-

from odoo import fields, models


class ClassRoom(models.Model):
    _name = 'school_management.class.room'
    _description = 'Class Room'

    name = fields.Char(string='Name')
    seat = fields.Integer(string='Seat')
