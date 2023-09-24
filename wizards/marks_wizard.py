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
    info = fields.Char(string='Info')

    @api.model
    def default_get(self, fields):
        this_wizard_field = super(MarksWizard, self).default_get(fields)
        result_obj = self.env['school_management.result'].browse(self.env.context.get('active_id'))
        exam_info = '<ul>'
        exam_info += f'<li><strong>Exam Title: </strong>{result_obj.exam.name}</li>'
        exam_info += f'<li><strong>Student Name: </strong>{result_obj.student.name}</li>'
        exam_info += f'<li><strong>Student Roll: </strong>{result_obj.student.roll}</li>'
        exam_info += '</ul>'
        this_wizard_field['info'] = exam_info
        return this_wizard_field

    def marks(self):
        pass
