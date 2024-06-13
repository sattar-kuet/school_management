# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo import api
import random
from ..constants import BLOOD_GROUP

class User(models.Model):
    _inherit = 'res.users'
    _description = 'School Management User'

    attendance_device_user_id = fields.Char()
    
    #*****************************************************************************
    #        Bellow fileds is for student
    #*****************************************************************************
    roll = fields.Char(string="Roll")
    # blood_group = fields.Selection(BLOOD_GROUP, string='Blood Group')
    # guardian = fields.Many2one("res.users", string="Guardian", domain=lambda self: [
    #         ("groups_id", "in", [self.env.ref("school_management.group_school_guardian").id])])
    # class_id = fields.Many2one("sm.class", string='Class')
    # section_id = fields.Many2one("sm.section", string='Class')
    #*****************************************************************************
    #        Bellow fileds is for teacher
    #*****************************************************************************
    # designation = fields.Many2one("sm.designation", string="Designation")


   

    
