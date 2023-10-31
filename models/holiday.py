# -*- coding: utf-8 -*-

from odoo import fields, models
import datetime


class HolidayConfig(models.Model):
    _name = 'school_management.holiday'
    _description = 'Holiday Config'

    title = fields.Char(string='Title')
    start_date = fields.Char(string='Start Date')
    end_date = fields.Char(string='End Date')

    @staticmethod
    def dates_for_year_range_and_specific_day(target_weekday, start_year, end_year):
        date_list = []
        for year in range(start_year, end_year + 1):
            date = datetime.date(year, 1, 1)
            while date.year == year:
                if date.weekday() == target_weekday:
                    date_list.append(date)
                date += datetime.timedelta(days=1)

        return date_list
