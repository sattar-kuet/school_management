from odoo import fields, models, api
class Section(models.Model):
    _name = 'sm.section'
    _description = 'Section'

    name = fields.Char(string="Name")