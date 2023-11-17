# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import datetime


class Notice(models.Model):
    _name = 'school_management.notice'
    _description = 'Notice'

    title = fields.Char(string='Title', required=True, )
    publishing_date = fields.Date(string="Publishing Date", default=fields.Date.today)
    content_type = fields.Selection([('text', 'Text'),('attachment', 'Attachment')])
    attachment = fields.Binary(string="Attachment")
    content = fields.Text(string="Content")

