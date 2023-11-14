# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api


class ClassConfig(models.Model):
    _name = 'sm.class_config'
    _description = 'School Management'

    name = fields.Char(string='Name', required=True)
    shift = fields.Many2one('school_management.shift', string="Shift")
    section = fields.Many2one('sm.section', string="Section")
    setup_lines = fields.Many2many('sm.class.setup.line', string="Setup Line")


class ClassSetupLine(models.Model):
    _name = 'sm.class.setup.line'
    _description = 'Class Setup line'


    subject = fields.Many2one('school_management.subject', string="Subject")
    teacher = fields.Many2one('res.users', string="Teacher")
    class_room = fields.Many2one('school_management.class.room', string="Class Room")
    start_at = fields.Char( string="Start at")
    end_at = fields.Char( string="End at")
    off_days = fields.Many2many('school_management.week.day', string="Off Days")


class Section(models.Model):
    _name = 'sm.section'
    _description = 'Section'


    name = fields.Char(string="Name")


