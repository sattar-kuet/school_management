# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Group(models.Model):
    _name = 'school_management.group'
    _description = 'Group'

    name = fields.Char(string='Name')
    name_bn = fields.Char(string='নাম')
