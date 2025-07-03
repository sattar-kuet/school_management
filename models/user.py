# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api
import random
from ..constants import BLOOD_GROUP
from odoo.exceptions import UserError
class User(models.Model):
    _inherit = 'res.users'
    _description = 'School Management User'

    attendance_device_user_id = fields.Char()
    
    #*****************************************************************************
    #        Bellow fileds is for student
    #*****************************************************************************
    roll = fields.Char(string="Roll")
    blood_group = fields.Selection(BLOOD_GROUP, string='Blood Group')
    guardian = fields.Many2one("res.users", string="Guardian", domain=lambda self: [
            ("groups_id", "in", [self.env.ref("school_management.group_school_guardian").id])])
    class_id = fields.Many2one("sm.class", string='Class')
    section_id = fields.Many2one("sm.section", string='Section')
    is_student = fields.Boolean()
    is_teacher = fields.Boolean()
    #*****************************************************************************
    #        Bellow fileds is for teacher
    #*****************************************************************************
    # designation = fields.Many2one("sm.designation", string="Designation")

    @api.model
    def create(self, vals):
        if 'is_student' in vals:
            roll = vals.get('roll')
            class_id = vals.get('class_id')
            section_id = vals.get('section_id')
            year = fields.Date.today().year
            # Ensure required values exist
            if not all([roll, class_id, section_id]):
                raise UserError("Roll, Class, and Section are required to generate login.")
            # Get class and section names from DB
            class_name = self.env['sm.class'].browse(class_id).name
            section_name = self.env['sm.section'].browse(section_id).name

            # Construct login
            login = f"{roll}-{class_name}-{section_name}-{year}"
            vals['login'] = login
        CreatedUser = super(User, self).create(vals)
        if 'groups_id' not in vals:
            if 'is_student' in vals:
                student_group = self.env.ref('school_management.group_school_student')
                if student_group:
                    CreatedUser.write({
                        'groups_id': [(4, student_group.id, 0)]
                    })
        return CreatedUser


   

    
