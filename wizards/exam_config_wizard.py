import base64
import io

import requests
import xlwt

from odoo import fields, models, http, api
from odoo.http import request
from odoo.tools import ustr


class ExamConfigWizard(models.TransientModel):
    _name = 'school_management.exam_config.wizard'
    _description = 'Exam Config wizard'

    
    type = fields.Selection([('new', 'New'), ('existing', 'Existing Config')] , default="new")
    existing_config = fields.Many2one('school_management.exam', string='Existing Config', domain="[('status', '!=', 'pending')]")


    def exam_config(self):
        pass

    