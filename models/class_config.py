# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api


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
                html_output += self.formatted_html('Subject',setup_info.subject.name)
                html_output += self.formatted_html('Teacher',setup_info.teacher.name)
                html_output += self.formatted_html('Class Room',setup_info.class_room.name)
                html_output += self.formatted_html('Class Start Time',setup_info.start_at)
                html_output += self.formatted_html('Class End Time',setup_info.end_at)
                html_output += self.formatted_html('Off Days',off_days)
                html_output += '</li>'
            html_output += '</ul>'
            record.computed_setup_info = html_output

    @staticmethod
    def formatted_html(title, value):
        return f'<button style="margin: 2px;" type="button" class="btn btn-info">' \
               f'{title} <span class="badge" style="background: #3c3737;font-size: 12px;padding: 4px;">' \
               f'{value}</span></button>'


class ClassSetupLine(models.Model):
    _name = 'sm.class.setup.line'
    _description = 'Class Setup line'

    subject = fields.Many2one('school_management.subject', string="Subject")
    teacher = fields.Many2one('res.users', string="Teacher")
    class_room = fields.Many2one('school_management.class.room', string="Class Room")
    start_at = fields.Char(string="Start at")
    end_at = fields.Char(string="End at")
    off_days = fields.Many2many('school_management.week.day', string="Off Days")


class Section(models.Model):
    _name = 'sm.section'
    _description = 'Section'

    name = fields.Char(string="Name")
