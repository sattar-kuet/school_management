from odoo import fields, models, api


class StudentWizard(models.TransientModel):
    _name = 'school_management.student.wizard'
    _description = 'Student Wizard'

    name = fields.Char(string='Name', required=True)
    roll = fields.Char(string="Roll", required=True)
    blood_group = fields.Selection([
        ('a+', 'A+'),
        ('b+', 'B+'),
        ('ab+', 'AB+'),
    ], string='Blood Group', required=True)
    student_group = fields.Many2one("school_management.group", string='Group', required=True)