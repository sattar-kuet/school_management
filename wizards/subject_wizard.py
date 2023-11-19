from odoo import fields, models, api


class SubjectWizard(models.TransientModel):
    _name = 'school_management.subject.wizard'
    _description = 'Subject Wizard'

    name = fields.Char(string='Name', required=True)
    has_practical = fields.Boolean(string='Has Practical')
    has_mcq = fields.Boolean(string='Has MCQ')
    has_written = fields.Boolean(string='Has Written')
    has_two_part = fields.Boolean(string='Has two Part')
    part1 = fields.Char(string='Part 1', compute='_compute_parts', store=True)
    part2 = fields.Char(string='Part 2', compute='_compute_parts', store=True)
    groups = fields.Many2many('school_management.group')
    mandatory = fields.Boolean(default=True)

    @api.depends('name', 'has_two_part')
    def _compute_parts(self):
        for record in self:
            if record.has_two_part and record.name:
                record.part1 = record.name + ' First Paper'
                record.part2 = record.name + ' Second Paper'
            else:
                record.part1 = False
                record.part2 = False

    def add_subject(self):
        if self.has_two_part:
            subject1 = self.env['school_management.subject'].create({
                'name': self.part1,
                'has_practical': self.has_practical,
                'has_mcq': self.has_mcq,
                'has_written': self.has_written,
                'groups': self.groups.ids,
                'mandatory': self.mandatory,
            })

            subject2 = self.env['school_management.subject'].create({
                'name': self.part2,
                'has_practical': self.has_practical,
                'has_mcq': self.has_mcq,
                'has_written': self.has_written,
                'groups': self.groups.ids,
                'mandatory': self.mandatory,
            })
            self.env['school_management.combined_subject'].create({
                'title': self.name,
                'subject': [subject1.id, subject2.id],
                'has_practical': self.has_practical,
                'has_mcq': self.has_mcq,
                'has_written': self.has_written,
                'groups': self.groups.ids,
                'mandatory': self.mandatory,
            })
        else:
            subject = self.env['school_management.subject'].create({
                'name': self.name,
                'has_practical': self.has_practical,
                'has_mcq': self.has_mcq,
                'has_written': self.has_written,
                'groups': self.groups.ids,
                'mandatory': self.mandatory,
            })

            self.env['school_management.combined_subject'].create({
                'title': self.name,
                'subject': [subject.id],
                'has_practical': self.has_practical,
                'has_mcq': self.has_mcq,
                'has_written': self.has_written,
                'groups': self.groups.ids,
                'mandatory': self.mandatory,
            })
        action = {
            'name': 'Subject',
            'view_mode': 'tree',
            'res_model': 'school_management.subject',
            'view_id': self.env.ref('school_management.view_subject_tree').id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        return action
