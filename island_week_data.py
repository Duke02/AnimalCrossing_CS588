import typing as tp
from enum import Enum

import numpy as np


class TurnipPattern(Enum):
    UNKNOWN = 'Unknown',
    DECREASING = 'Decreasing',
    RANDOM = 'Random',
    HIGH_SPIKE = 'High Spike',
    SMALL_SPIKE = 'Small Spike',
    EMPTY = 'empty'

    def __repr__(self):
        return self.value


class IslandWeekData:
    """
    Data for a single island for an entire week. May have values missing.
    """

    def __init__(self, owner: str, island_name: str, week_num: int, prices: tp.List[tp.Union[int, None]],
                 purchase_price: tp.Union[None, int], previous_pattern: tp.Union[None, TurnipPattern],
                 current_pattern: tp.Union[None, TurnipPattern]):
        """
        Initializes the sample of data from an island's local turnip price market.
        :param owner: An identifier (not too important) of the owner of the island.
        :param island_name: An identifier (not too important) of the island name.
        :param week_num: An identifier that designates which week this sample is from according to the spreadsheet.
        :param prices: A list of 12 values that turnips could have been sold for at this island's local market.
        :param purchase_price: The price the owner purchased turnips for on Sunday morning of this week.
        :param previous_pattern: The pattern for the previous week for this island
        :param current_pattern: The current pattern for this week for the island. If None will be predicted.
        """
        self.owner: str = owner
        self.island_name: str = island_name
        self.week_num: int = week_num
        self.prices: tp.List[tp.Union[None, int]] = prices
        self.purchase_price: int = purchase_price
        self.previous_pattern: tp.Union[None, TurnipPattern] = previous_pattern
        self.current_pattern: tp.Union[None, TurnipPattern] = current_pattern

    def __str__(self):
        return f'Island {self.island_name} ({self.owner}), W{self.week_num}, Purchase: {self.purchase_price},' + \
               f' Curr Pattern: {self.current_pattern}, Prev Pattern: {self.previous_pattern}, ' + \
               f'Prices: [{", ".join([str(price) for price in self.prices])}]'

    def predict_current_pattern(self, model):
        """
        Predicts the current pattern based on the prices in this sample.
        TO BE IMPLEMENTED.
        :param model: The classifier that provides multiple patterns with their confidences.
        :return: The predicted current pattern.
        """
        pass

    def to_numpy(self):
        out: np.ndarray = np.asarray([price - self.purchase_price for price in self.prices])
        return out
