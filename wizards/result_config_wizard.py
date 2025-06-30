from odoo import fields, models, api


class ConfigWizard(models.TransientModel):
    _name = 'school_management.config.wizard'
    _description = 'Config wizard'

    written_pass_mark = fields.Float(string='Written Pass Marks')
    written_max_mark = fields.Float(string='Written Max Marks')
    mcq_pass_mark = fields.Float(string='MCQ Pass Marks')
    mcq_max_mark = fields.Float(string='MCQ Max Marks')
    practical_pass_mark = fields.Float(string='Practical Pass Marks')
    practical_max_mark = fields.Float(string='Practical Max Marks')
    total_pass_mark = fields.Float(string='Total Pass Marks')

    subject_name = fields.Char(string='Subject Name')
    has_practical = fields.Boolean()
    has_mcq = fields.Boolean()
    has_written = fields.Boolean()
    has_two_part = fields.Boolean()
    subject_part1 = fields.Many2one('sm.subject')
    subject_part1_title = fields.Char(string='One Part')
    subject_part1_written_max_mark = fields.Float(string='Subject Part1 Written Max Marks')
    subject_part1_mcq_max_mark = fields.Float(string='Subject Part1 MCQ Max Marks')
    subject_part1_practical_max_mark = fields.Float(string='Subject Part1 Practical Max Marks')

    subject_part2 = fields.Many2one('sm.subject')
    subject_part2_title = fields.Char(string='Another Part')
    subject_part2_written_max_mark = fields.Float(string='Subject Part2 Written Max Marks')
    subject_part2_mcq_max_mark = fields.Float(string='Subject Part2 MCQ Max Marks')
    subject_part2_practical_max_mark = fields.Float(string='Subject Part2 Practical Max Marks')

    status = fields.Selection([('generated', 'System Generated'), ('configured', 'Configured')], default='generated')

    @api.model
    def default_get(self, fields):
        this_wizard_fields = super(ConfigWizard, self).default_get(fields)
        result_config = self.env['school_management.result_config'].browse(self.env.context.get('active_id'))
        this_wizard_fields['has_mcq'] = result_config.subject.has_mcq
        this_wizard_fields['has_written'] = result_config.subject.has_written
        this_wizard_fields['has_practical'] = result_config.subject.has_practical

        this_wizard_fields['written_pass_mark'] = result_config.written_pass_mark
        this_wizard_fields['written_max_mark'] = result_config.written_max_mark
        this_wizard_fields['mcq_pass_mark'] = result_config.mcq_pass_mark
        this_wizard_fields['mcq_max_mark'] = result_config.mcq_max_mark
        this_wizard_fields['practical_pass_mark'] = result_config.practical_pass_mark
        this_wizard_fields['practical_max_mark'] = result_config.practical_max_mark
        this_wizard_fields['total_pass_mark'] = result_config.total_pass_mark

        this_wizard_fields['subject_name'] = result_config.subject.title
        has_two_part = len(result_config.subject.subject.ids) == 2
        this_wizard_fields['has_two_part'] = has_two_part

        if has_two_part:
            this_wizard_fields['subject_part1'] = result_config.subject.subject.ids[0]
            subject1_record = self.env['sm.subject'].browse(result_config.subject.subject.ids[0])
            this_wizard_fields['subject_part1_title'] = subject1_record.name
            this_wizard_fields['subject_part2'] = result_config.subject.subject.ids[1]
            subject2_record = self.env['sm.subject'].browse(result_config.subject.subject.ids[1])
            this_wizard_fields['subject_part2_title'] = subject2_record.name

            for two_part_setup_line in result_config.two_part_setup_line:
                if two_part_setup_line.subject.id == subject1_record.id:
                    this_wizard_fields['subject_part1_written_max_mark'] = two_part_setup_line.written_max_mark
                    this_wizard_fields['subject_part1_mcq_max_mark'] = two_part_setup_line.mcq_max_mark
                    this_wizard_fields['subject_part1_practical_max_mark'] = two_part_setup_line.practical_max_mark
                else:
                    this_wizard_fields['subject_part2_written_max_mark'] = two_part_setup_line.written_max_mark
                    this_wizard_fields['subject_part2_mcq_max_mark'] = two_part_setup_line.mcq_max_mark
                    this_wizard_fields['subject_part2_practical_max_mark'] = two_part_setup_line.practical_max_mark

        return this_wizard_fields

    def result_config_button(self):

        result_config = self.env['school_management.result_config'].browse(self.env.context.get('active_id'))
        result_config.written_pass_mark = self.written_pass_mark
        result_config.written_max_mark = self.written_max_mark
        result_config.mcq_pass_mark = self.mcq_pass_mark
        result_config.mcq_max_mark = self.mcq_max_mark
        result_config.practical_pass_mark = self.practical_pass_mark
        result_config.practical_max_mark = self.practical_max_mark
        result_config.total_pass_mark = self.total_pass_mark
        part_one_config = self.env['sm.two.part.mark.config'].search([('exam', '=', result_config.exam.id),
                                                    ('subject', '=', self.subject_part1.id)], limit=1)
        two_part_setup_line = []
        part_one_config_data = {
            'exam': result_config.exam.id,
            'subject': self.subject_part1.id,
            'written_max_mark': self.subject_part1_written_max_mark,
            'mcq_max_mark': self.subject_part1_mcq_max_mark,
            'practical_max_mark': self.subject_part1_practical_max_mark
        }
        if part_one_config:
            part_one_config.write(part_one_config_data)
            two_part_setup_line.append(part_one_config.id)
        else:
            new_part_one_config = part_one_config.create(part_one_config_data)
            two_part_setup_line.append(new_part_one_config.id)

        part_two_config = self.env['sm.two.part.mark.config'].search([('exam', '=', result_config.exam.id),
                                                                      ('subject', '=', self.subject_part2.id)], limit=1)
        part_two_config_data = {
            'exam': result_config.exam.id,
            'subject': self.subject_part2.id,
            'written_max_mark': self.subject_part2_written_max_mark,
            'mcq_max_mark': self.subject_part2_mcq_max_mark,
            'practical_max_mark': self.subject_part2_practical_max_mark
        }
        if part_two_config:
            part_two_config.write(part_two_config_data)
            two_part_setup_line.append(part_two_config.id)
        else:
            new_part_two_config = part_two_config.create(part_two_config_data)
            two_part_setup_line.append(new_part_two_config.id)

        result_config.two_part_setup_line = two_part_setup_line

        result_config.status = 'configured'

        if self.env['school_management.result_config'].search_count(
                [('exam', '=', result_config.exam.id), ('status', '=', 'generated')]) == 0:
            self.env['school_management.exam'].browse(result_config.exam.id).write({
                'status': 'setup_done'
            })
