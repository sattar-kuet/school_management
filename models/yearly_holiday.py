# -*- coding: utf-8 -*-

from odoo import fields, models
import datetime


class YearlyHolidayConfig(models.Model):
    _name = 'school_management.yearly.holiday'
    _description = 'Holiday Config'

    name = fields.Char(string='Title')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

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

    def generate(self):
        cr = self._cr
        sql_query = f"TRUNCATE TABLE school_management_yearly_holiday"
        cr.execute(sql_query)

        weekly_holiday = self.env['school_management.weekly.holiday'].search([], limit=1)
        session = self.env['school_management.session'].search([], limit=1)
        for weekly_off_day in weekly_holiday.weekly_off_days:
            date_list = self.dates_for_year_range_and_specific_day(weekly_off_day.value, session.start_year,
                                                                   session.end_year)
            for date in date_list:
                self.env['school_management.yearly.holiday'].create({
                    'name': 'সাপ্তাহিক ছুটি',
                    'start_date': date,
                    'end_date': date
                })
