import base64
import io

import requests
import xlwt

from odoo import fields, models, http, api
from odoo.http import request
from odoo.tools import ustr


class ConfigWizard(models.TransientModel):
    _name = 'school_management.config.wizard'
    _description = 'Config wizard'

    written_pass_mark = fields.Float(string='Written Pass Mark')
    written_max_mark = fields.Float(string='Written Max Mark')
    mcq_pass_mark = fields.Float(string='MCQ Pass Mark')
    mcq_max_mark = fields.Float(string='MCQ Max Mark')
    practical_pass_mark = fields.Float(string='Practical Pass Mark')
    practical_max_mark = fields.Float(string='Practical Max Mark')

    

    def result_config_button(self):
        pass
