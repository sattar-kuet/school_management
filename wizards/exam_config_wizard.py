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

    type = fields.Selection([('new', 'New'), ('existing', 'Existing Config')], default="new")
    existing_config = fields.Many2one('school_management.exam', string='Existing Config',
                                      domain="[('status', '!=', 'pending')]")

    def exam_config(self):
        exam_id = self.env.context.get('active_id')
        exam_obj = self.env['school_management.exam'].browse(exam_id)
        if self.type == 'existing':
            existing_exam_id = self.existing_config.id
            result_configs = self.env['school_management.result_config'].search([('exam', '=', existing_exam_id)])
            for result_config in result_configs:
                result_config.write({'exam': [(4, exam_id)]})
            exam_obj.status = 'setup_done'
        else:
            action = {
                'name': 'Result Config',
                'view_mode': 'tree',
                'res_model': 'school_management.result_config',
                'view_id': self.env.ref('school_management.view_result_config_tree').id,
                'type': 'ir.actions.act_window',
                'target': 'current'
            }
            if self.env['school_management.result_config'].search_count([('exam', '=', exam_id)]) != 0:
                if self.env['school_management.result_config'].search_count(
                        [('exam', '=', exam_id), ('status', '=', 'pending')]) == 0:
                    exam_obj.status = 'setup_done'
                return action
            subject_config = self.env['school_management.subject_config'].search(
                [('class_config', '=', exam_obj.class_config.id)])
            combined_subject_list = self.env['school_management.combined_subject'].search(
                [('subject', 'in', subject_config.subject.ids)])

            for combined_subject in combined_subject_list:
                result_config_vals = {
                    'subject': combined_subject.id,
                    'exam': [exam_id],
                    'written_pass_mark': 0,
                    'written_max_mark': 0,
                    'mcq_pass_mark': 0,
                    'mcq_max_mark': 0,
                    'practical_pass_mark': 0,
                    'practical_max_mark': 0,
                    'status': 'generated',
                }
                self.env['school_management.result_config'].create(result_config_vals)

            return action
