import typing as tp
from enum import Enum

import numpy as np


class TurnipPattern(Enum):
    UNKNOWN = ('Unknown', -1)
    EMPTY = ('empty', 0)
    DECREASING = ('Decreasing', 1)
    RANDOM = ('Random', 2)
    HIGH_SPIKE = ('High Spike', 3)
    SMALL_SPIKE = ('Small Spike', 4)

    def __repr__(self):
        return self.value[0]


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
        self.current_pattern = model.predict(self.to_numpy())[0]
        return self

    def get_pattern_modifier(self) -> float:
        if not self.has_patterns_populated():
            return 5.0 / 4.0
        return float(self.previous_pattern.value[1]) / 4.0

    def to_numpy(self):
        out: np.ndarray = np.asarray([price - self.purchase_price if price else (10 ** -5) for price in self.prices]) \
                          * self.get_pattern_modifier()
        return out

    def to_numpy_regression(self):
        return self.to_numpy() * self.get_pattern_modifier()

    def is_valid(self, min_prices: int) -> bool:
        return len([p for p in self.prices if p]) >= min_prices

    def is_perfect(self) -> bool:
        return all(self.prices) and \
               len(self.prices) >= 12 and \
               self.has_patterns_populated()

    def has_patterns_populated(self) -> bool:
        return (self.current_pattern not in {TurnipPattern.EMPTY, TurnipPattern.UNKNOWN}) and \
               (self.previous_pattern not in {TurnipPattern.EMPTY, TurnipPattern.UNKNOWN})
