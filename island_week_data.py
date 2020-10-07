import typing as tp
from enum import Enum


class TurnipPattern(Enum):
    UNKNOWN = 'Unknown',
    DECREASING = 'Decreasing',
    RANDOM = 'Random',
    HIGH_SPIKE = 'High Spike',
    SMALL_SPIKE = 'Small Spike'

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
