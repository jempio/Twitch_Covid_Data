"""Covid Data Manipulation

Description
===============================

Create a dataclass to store the information from covid_by_year.csv
Also create function to calculate total cases in a month
from the dataset.


Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Winston Chieng, Justin Li, Derrick Cho, Sabarish Gnanamoorthy
"""

from dataclasses import dataclass
import csv


@dataclass
class CovidData:
    """The daily data for covid cases in a country

        Instance Attributes:
            - date: date of data
            - country: country of data
            - cumulative_total_cases: all total cases in a country
            - daily_new_cases: daily number of new cases in a country
            - active_cases: all active cases in a country
            - cumulative_total_deaths: all total deaths from covid in a country
            - daily_new_deaths: daily number of deaths from covid in a country

        """

    date: str
    country: str
    cumulative_total_cases: float
    daily_new_cases: float
    active_cases: float
    cumulative_total_deaths: float
    daily_new_deaths: float


def load_data_country(filename: str, country: str, year: list[int]) -> list[CovidData]:
    """Return a list of CovidData objects for a game, for each year specified.

    """
    # ACCUMULATOR inputs_so_far: The Twitch data parsed from filename so far
    inputs_so_far = []

    with open(filename) as x:
        reader = csv.reader(x, delimiter=',')
        next(reader)  # skip the header

        for row in reader:
            list_of_dates = row[0].split("-")
            split_year = list_of_dates[0]
            if int(split_year) in year and str(row[1]) == country:
                assert len(row) == 7, 'Expected every row to contain 7 elements.'
                for i in range(len(row)):
                    if row[i] == '':
                        row[i] = '0.0'  # gets rid of any empty values in row
                    # row is a list of strings
                covid_data = CovidData(str(row[0]), str(row[1]), float(row[2]), float(row[3]),
                                       float(row[4]), float(row[5]), float(row[6]))
                inputs_so_far.append(covid_data)

    return inputs_so_far


def total_cases(data_list: list[CovidData], year: int,
                month: int) -> int:
    """Return the total covid cases for a country in a month

    """
    months_with_31_days = [1, 3, 5, 7, 8, 10, 12]
    months_with_30_days = [11, 4, 6, 9]
    cases_so_far = 0
    for data in data_list:
        valid_year = int(data.date.split("-")[0])
        valid_month = int(data.date.split("-")[1])
        valid_day = int(data.date.split("-")[2])
        if int(valid_year) == year and int(valid_month) == month:
            cases_so_far += data.daily_new_cases
        if valid_month == month and valid_month in months_with_30_days and valid_day == 30:
            return int(cases_so_far)
        elif valid_month == month and valid_month in months_with_31_days and valid_day == 31:
            return int(cases_so_far)
        else:
            if valid_month == month and valid_month == 2 and year == 2020 and valid_day == 29:
                return int(cases_so_far)
            if valid_month == month and valid_month == 2 and year == 2021 and valid_day == 28:
                return int(cases_so_far)
