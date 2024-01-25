# -*- coding: utf-8 -*-
from odoo import fields, models
from datetime import datetime


class ClassConfig(models.Model):
    _name = 'sm.class_config'
    _description = 'School Management'

    name = fields.Char(string='Name', required=True)
    has_group = fields.Boolean()
    shift = fields.Many2one('school_management.shift', string="Shift")
    section = fields.Many2one('sm.section', string="Section")
    setup_lines = fields.Many2many('sm.class.setup.line', string="Setup Line")
    computed_setup_info = fields.Text(string='Configuration', compute='_compute_setup_info')

    def _compute_setup_info(self):
        for record in self:
            html_output = '<ul>'
            for setup_info in record.setup_lines:
                off_days = ''
                for off_day in setup_info.off_days:
                    off_days += off_day.name + '  '
                html_output += '<li>'
                html_output += self.formatted_html('fa-book', setup_info.subject.name)
                html_output += self.formatted_html('fa-user', setup_info.teacher.name)
                html_output += self.formatted_html('fa-university', setup_info.class_room.name)
                class_time = '-'
                # if setup_info.start_at_am_pm and setup_info.end_at_am_pm:
                #   class_time = f'{setup_info.start_at_am_pm} to {setup_info.end_at_am_pm}'
                html_output += self.formatted_html('fa-clock-o', class_time)
                html_output += self.formatted_html('fa-times', off_days)
                html_output += '</li>'
            html_output += '</ul>'
            record.computed_setup_info = html_output

    @staticmethod
    def formatted_html(fa_icon, value):
        return f'<button style="margin: 2px;" type="button" class="btn btn-info">' \
               f'<span class="fa {fa_icon}" style="color: #fff;"></span> ' \
               f'<span class="badge" style="background: #3c3737;font-size: 12px;padding: 4px;">{value}</span>' \
               f'</button>'


class ClassSetupLine(models.Model):
    _name = 'sm.class.setup.line'
    _description = 'Class Setup line'

    subject = fields.Many2one('school_management.subject', string="Subject")
    teacher = fields.Many2one('res.users', string="Teacher", domain=lambda self: [
        ("groups_id", "in", [self.env.ref("school_management.group_school_teacher").id])])
    class_room = fields.Many2one('school_management.class.room', string="Class Room")
    start_at = fields.Char(string="Start at")
    start_at_am_pm = fields.Char(string="Start at", compute="_compute_start_at_am_pm")
    end_at = fields.Char(string="End at")
    end_at_am_pm = fields.Char(string="End at", compute="_compute_end_at_am_pm")
    off_days = fields.Many2many('school_management.week.day', string="Off Days")

    def _compute_start_at_am_pm(self):
        for record in self:
            if record.start_at:
                time_obj = datetime.strptime(record.start_at, "%H:%M")
                record.start_at_am_pm = time_obj.strftime("%I:%M %p")

    def _compute_end_at_am_pm(self):
        for record in self:
            if record.end_at:
                time_obj = datetime.strptime(record.end_at, "%H:%M")
                record.end_at_am_pm = time_obj.strftime("%I:%M %p")


class Section(models.Model):
    _name = 'sm.section'
    _description = 'Section'

    name = fields.Char(string="Name")
