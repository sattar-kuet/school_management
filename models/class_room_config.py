# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime


class ClassRoomConfig(models.Model):
    _name = 'school_management.class.room.config'
    _description = 'Seat'

    class_room = fields.Many2one('school_management.class.room', string='Class Room')
    shift = fields.Many2one('school_management.shift', string='Shift')
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    subject = fields.Many2one('school_management.subject', string='Subject')
    week_days = fields.Many2one('school_management.week.day', string='Subject')
