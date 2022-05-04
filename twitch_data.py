"""Twitch Data Manipulation

Description
===============================

Create dataclasses to store the information from twitch_game_data.csv
and twitch_global.csv. Also create functions to calculate average watchtime of streams
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
class TwitchDataGame:
    """The monthly data for a game on Twitch

    Instance Attributes:
        - name: name of game
        - rank: rank of the game in terms of popularity on twitch
        - month: month of data
        - year: year of data
        - hours_watched: total hours watched by viewers
        - hours_streamed: total hours streamed by streamers
        - peak_viewers: peak viewers watching the game at one time
        - peak_channels: peak channels livestreaming at one time
        - streamers: streamers who played the game on this month
        - avg_viewers: average number of viewers
        - avg_channels: average number of channels
        - avg_viewer_ratio: ratio of viewers to channels


    """
    name: str
    rank: int
    month: int
    year: int
    hours_watched: int
    hours_streamed: int
    peak_viewers: int
    peak_channels: int
    streamers: int
    avg_viewers: int
    avg_channels: int
    avg_viewer_ratio: float


@dataclass
class TwitchDataGlobal:
    """The monthly data for all active stats on Twitch

    Instance Attributes:
        - year: year of data
        - month: month of data
        - hours_watched: total hours watched by viewers
        - avg_viewers: average number of viewers
        - peak_viewers: peak viewers on twitch at one time
        - streams: number of streams
        - avg_channels: average number of channels
        - games_streamed: number of different games streamed that month

    """

    year: int
    month: int
    hours_watched: int
    avg_viewers: int
    peak_viewers: int
    streams: int
    avg_channels: int
    games_streamed: int


def load_data_game(filename: str, game: str, years: list[int]) -> list[TwitchDataGame]:
    """Return a list of TwitchDataGame objects for a game, for each year specified.
.
    """
    # ACCUMULATOR inputs_so_far: The Twitch data parsed from filename so far
    inputs_so_far = []

    with open(filename) as x:
        reader = csv.reader(x, delimiter=',')
        next(reader)  # skip the header

        for row in reader:
            if str(row[0]) == game and int(row[3]) in years:
                assert len(row) == 12, 'Expected every row to contain 12 elements.'
                # row is a list of strings
                twitch_data = TwitchDataGame(str(row[0]), int(row[1]), int(row[2]), int(row[3]),
                                             int(row[4]), int(row[5]), int(row[6]), int(row[7]),
                                             int(row[8]), int(row[9]), int(row[10]), float(row[11]))
                inputs_so_far.append(twitch_data)

    return inputs_so_far


def load_data_global(filename: str, years: list[int]) -> list[TwitchDataGlobal]:
    """Return a list of TwitchDataGlobal objects for each year specified.
.
    """
    # ACCUMULATOR inputs_so_far: The Twitch data parsed from filename so far
    inputs_so_far = []

    with open(filename) as x:
        reader = csv.reader(x, delimiter=',')
        next(reader)  # skip the header

        for row in reader:
            if int(row[0]) in years:
                assert len(row) == 8, 'Expected every row to contain 8 elements.'
                # row is a list of strings
                twitch_data = TwitchDataGlobal(int(row[0]), int(row[1]), int(row[2]), int(row[3]),
                                               int(row[4]), int(row[5]), int(row[6]), int(row[7]))
                inputs_so_far.append(twitch_data)

    return inputs_so_far


def average_viewership(data_list: list[TwitchDataGame] or list[TwitchDataGlobal],
                       start_month: int, end_month: int) -> (int, int):
    """Return the average hours watched and viewers for a game between input months

    """
    hours_watched_avg = 0
    viewers_avg = 0
    valid_months = list(range(start_month, end_month + 1))
    for data in data_list:
        if data.month in valid_months:
            hours_watched_avg += data.hours_watched
            viewers_avg += data.avg_viewers

    return hours_watched_avg // len(valid_months), viewers_avg // len(valid_months)


def average_viewership_v2(data_list: list[TwitchDataGame] or list[TwitchDataGlobal],
                          month: int) -> (int, int):
    """Return the average hours watched and viewers for a game between input months

    """
    hours_watched_avg = 0
    viewers_avg = 0
    for data in data_list:
        if data.month == month:
            hours_watched_avg += data.hours_watched
            viewers_avg += data.avg_viewers

    return hours_watched_avg, viewers_avg
