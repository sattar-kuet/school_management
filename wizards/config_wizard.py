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
    has_practical = fields.Boolean()
    has_mcq = fields.Boolean()
    has_written = fields.Boolean()
    status = fields.Selection([('generated', 'System Generated'), ('configured', 'Configured')], defualt='generated')

    @api.model
    def default_get(self, fields):
        this_wizard_fields = super(ConfigWizard, self).default_get(fields)
        result_config = self.env['school_management.result_config'].browse(self.env.context.get('active_id'))
        this_wizard_fields['has_mcq'] = result_config.subject.has_mcq
        this_wizard_fields['has_written'] = result_config.subject.has_written
        this_wizard_fields['has_practical'] = result_config.subject.has_practical

        this_wizard_fields['written_pass_mark'] = result_config.written_pass_mark
        this_wizard_fields['written_max_mark'] = result_config.written_max_mark
        this_wizard_fields['mcq_pass_mark'] = result_config.mcq_pass_mark
        this_wizard_fields['mcq_max_mark'] = result_config.mcq_max_mark
        this_wizard_fields['practical_pass_mark'] = result_config.practical_pass_mark
        this_wizard_fields['practical_max_mark'] = result_config.practical_max_mark

        this_wizard_fields['subject_name'] = result_config.subject.title

        return this_wizard_fields

    def result_config_button(self):
        result_config = self.env['school_management.result_config'].browse(self.env.context.get('active_id'))
        result_config.written_pass_mark = self.written_pass_mark
        result_config.written_max_mark = self.written_max_mark
        result_config.mcq_pass_mark = self.mcq_pass_mark
        result_config.mcq_max_mark = self.mcq_max_mark
        result_config.practical_pass_mark = self.practical_pass_mark
        result_config.practical_max_mark = self.practical_max_mark
