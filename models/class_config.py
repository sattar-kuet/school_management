# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api


class ClassConfig(models.Model):
    _name = 'sm.class_config'
    _description = 'School Management'

    name = fields.Char(string='Name', required=True)
    shift = fields.Many2one('school_management.shift', String="Shift")
    section = fields.Many2one('sm.section', String="Section")
    setup_lines = fields.Many2many('sm.class.setup.line')


class ClassSetupLine(models.Model):
    _name = 'sm.class.setup.line'
    _description = 'Class Setup line'


    subject = fields.Many2one('school_management.subject', String="Subject")
    teacher = fields.Many2one('res.users', String="Teacher")
    class_room = fields.Many2one('school_management.class.room', String="Class Room")
    start_at = fields.Char( String="Start at")
    end_at = fields.Char( String="End at")
    off_days = fields.Many2many('school_management.week.day', String="Off Days")


class Section(models.Model):
    _name = 'sm.section'
    _description = 'Section'


    name = fields.Char(String="Name")


