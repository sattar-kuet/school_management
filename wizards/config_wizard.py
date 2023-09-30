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

    subject_name = fields.Char(string='Subject Name')
    has_practical = fields.Boolean(compute="_has_practical")
    has_mcq = fields.Boolean(compute="_has_mcq")
    has_written = fields.Boolean(compute="_has_written")
    status = fields.Selection([('generated', 'System Generated'), ('configured', 'Configured')], defualt='generated')

    @api.model
    def default_get(self, fields):
        this_wizard_fields = super(ConfigWizard, self).default_get(fields)
        result_config = self.env['school_management.result_config'].browse(self.env.context.get('active_id'))
        this_wizard_fields['has_mcq'] = result_config.subject.has_mcq
        this_wizard_fields['has_written'] = result_config.subject.has_written
        this_wizard_fields['has_practical'] = result_config.subject.has_practical
        this_wizard_fields['subject_name'] = result_config.subject.title

        return this_wizard_fields

    def result_config_button(self):
        pass
