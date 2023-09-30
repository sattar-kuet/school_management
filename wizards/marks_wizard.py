import base64
import io

import requests
import xlwt

from odoo import fields, models, http, api
from odoo.http import request
from odoo.tools import ustr


class MarksWizard(models.TransientModel):
    _name = 'school_management.marks.wizard'
    _description = 'Add marks wizard'

    written_mark = fields.Char(string='Written Mark')
    mcq_mark = fields.Char(string='MCQ Mark')
    practical_mark = fields.Char(string='Practical Mark')
    info_left = fields.Char(string='Exam Info')
    info_right = fields.Char(string='Student Info')
    has_written = fields.Boolean()
    has_mcq = fields.Boolean()
    has_practical = fields.Boolean()
    @api.model
    def default_get(self, fields):
        this_wizard_field = super(MarksWizard, self).default_get(fields)
        result_obj = self.env['school_management.result'].browse(self.env.context.get('active_id'))
        info_left = '<ul>'
        info_left += f'<li><strong>Exam Title: </strong>{result_obj.exam.name}</li>'
        info_left += f'<li><strong>Subject: </strong>{result_obj.subject.name}</li>'
        info_left += f'<li><strong>Class: </strong>{result_obj.exam.class_config.name}</li>'
        info_left += '</ul>'

        info_right = '<ul>'
        info_right += f'<li><strong>Student Name: </strong>{result_obj.student.name}</li>'
        info_right += f'<li><strong>Student Roll: </strong>{result_obj.student.roll}</li>'
        info_right += '</ul>'

        this_wizard_field['info_left'] = info_left
        this_wizard_field['info_right'] = info_right

        this_wizard_field['written_mark'] = result_obj.written_mark
        this_wizard_field['mcq_mark'] = result_obj.mcq_mark
        this_wizard_field['practical_mark'] = result_obj.practical_mark

        this_wizard_field['has_written'] = result_obj.subject.has_written
        this_wizard_field['has_mcq'] = result_obj.subject.has_mcq
        this_wizard_field['has_practical'] = result_obj.subject.has_practical
        return this_wizard_field

    def marks(self):
        print(self.env.context.get('active_id'))
        self.env['school_management.result'].browse(self.env.context.get('active_id')).write({
            'written_mark': self.written_mark,
            'mcq_mark': self.mcq_mark,
            'practical_mark': self.practical_mark,
            'status': 'done'
        })

