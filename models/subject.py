# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Subject(models.Model):
    _name = 'school_management.subject'
    _description = 'Subject Management'

    name = fields.Char(string='Name', required=True)
    has_practical = fields.Boolean(string='Has Practical')
    has_mcq = fields.Boolean(string='Has MCQ')
    has_written = fields.Boolean(string='Has Written')
    groups = fields.Many2many('school_management.group')
    mandatory = fields.Boolean(default=True)

    def write(self, vals):
        combined_subject = self.env['school_management.combined_subject'].search([('subject', 'in', self.ids)], limit=1)

        print('*' * 100, combined_subject)
        print('*' * 100, vals)
        if combined_subject:
            self.update_subject('school_management_combined_subject', combined_subject.id, vals)
            combined_subject_ids = combined_subject.mapped('subject.id')
            remaining_subject_ids = list(set(combined_subject_ids) - set(self.ids))
            if remaining_subject_ids:
                self.update_subject('school_management_subject', remaining_subject_ids[0], vals)

        return super(Subject, self).write(vals)

    def update_subject(self, table_name, id, vals):
        cr = self._cr
        if 'has_practical' in vals:
            sql_query = f"UPDATE {table_name} SET has_practical = %s WHERE id = %s"
            cr.execute(sql_query, (vals['has_practical'], id))
        elif 'has_mcq' in vals:
            sql_query = f"UPDATE {table_name} SET has_mcq = %s WHERE id = %s"
            cr.execute(sql_query, (vals['has_mcq'], id))
        elif 'has_written' in vals:
            sql_query = f"UPDATE {table_name} SET has_written = %s WHERE id = %s"
            cr.execute(sql_query, (vals['has_written'], id))
        elif 'groups' in vals:
            sql_query = f"UPDATE {table_name} SET groups = %s WHERE id = %s"
            cr.execute(sql_query, (vals['groups'], id))
        elif 'mandatory' in vals:
            sql_query = f"UPDATE {table_name} SET mandatory = %s WHERE id = %s"
            cr.execute(sql_query, (vals['mandatory'], id))
