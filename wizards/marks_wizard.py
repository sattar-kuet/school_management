import base64
import io

import requests
import xlwt

from odoo import fields, models, http
from odoo.http import request
from odoo.tools import ustr


class MarksWizard(models.TransientModel):
    _name = 'school_management.marks.wizard'
    _description = 'Add marks wizard'

    written_mark = fields.Char(string='Written Mark')
    mcq_mark = fields.Char(string='MCQ Mark')
    practical_mark = fields.Char(string='Practical Mark')

    

    def marks(self):
        pass
