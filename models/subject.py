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
        response = super(Subject, self).write(vals)
        combined_subject = self.env['school_management.combined_subject'].search([('subject', 'in', self.ids)], limit=1)
        if combined_subject:
            self.update_subject('school_management_combined_subject', combined_subject.id, self.groups.ids, vals)
            combined_subject_ids = combined_subject.mapped('subject.id')
            remaining_subject_ids = list(set(combined_subject_ids) - set(self.ids))

            if remaining_subject_ids:
                self.update_subject('school_management_subject', remaining_subject_ids[0], self.groups.ids, vals)

        return response

    def update_subject(self, table_name, subject_id, group_ids, vals):
        cr = self._cr
        if 'has_practical' in vals:
            sql_query = f"UPDATE {table_name} SET has_practical = %s WHERE id = %s"
            cr.execute(sql_query, (vals['has_practical'], subject_id))
        if 'has_mcq' in vals:
            sql_query = f"UPDATE {table_name} SET has_mcq = %s WHERE id = %s"
            cr.execute(sql_query, (vals['has_mcq'], subject_id))
        if 'has_written' in vals:
            sql_query = f"UPDATE {table_name} SET has_written = %s WHERE id = %s"
            cr.execute(sql_query, (vals['has_written'], subject_id))
        if 'groups' in vals:
            group_table = 'school_management_group_school_management_subject_rel'
            if table_name == 'school_management_combined_subject':
                group_table = 'school_management_combined_subject_school_management_group_rel'
            self.update_group(group_table, group_ids, subject_id)
        if 'mandatory' in vals:
            sql_query = f"UPDATE {table_name} SET mandatory = %s WHERE id = %s"
            cr.execute(sql_query, (vals['mandatory'], subject_id))

    def update_group(self, table_name, group_ids, subject_id):
        # *******************************************  ATTENTION PLEASE  ********************************************
        # HERE YOU CAN'T USE ORM. YOU HAVE TO WRITE RAW SQL ONLY
        # BECAUSE YOU DIDN'T CREATE ANY MODEL FOR 'school_management_combined_subject_school_management_group_rel'
        # ***********************************************************************************************************

        cr = self._cr
        column_name = 'school_management_subject_id'
        if table_name == 'school_management_combined_subject_school_management_group_rel':
            column_name = 'school_management_combined_subject_id'

        sql_query = f"DELETE FROM {table_name}  WHERE {column_name} = %s"
        cr.execute(sql_query, (subject_id,))

        for group_id in group_ids:
            sql_query = f"INSERT INTO {table_name}  ({column_name},school_management_group_id) VALUES(%s,%s)"
            cr.execute(sql_query, (subject_id, group_id))
