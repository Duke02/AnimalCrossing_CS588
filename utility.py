"""
Utility file to help determine different aspects about the data.
"""
import datetime as dt
import os
import pickle
import typing as tp

import numpy as np

from constants import MIN_NUM_PRICES, MODEL_FILEPATH
from island_week_data import TurnipPattern, IslandWeekData


def _levenshtein_distance(str1: str, str2: str, max_distance: int = -1) -> tp.Tuple[int, bool]:
    """
    My favorite distance metric for strings. Calculates the number of substitutions, deletions, and additions must be
    made to str1 in order for it to be made into str2.
    :param str1: The first string to compare.
    :param str2: The second string to compare.
    :param max_distance: The function will stop if the distance is over the max_distance. If equal to -1 (the default), the function won't stop early.
    :return: A tuple containing the resulting distance and whether the function was able to fully calculate the metric.
    """
    # Stop early in case the strings are equal.
    if str1 == str2:
        return 0, True

    # This code has been adapted from
    # https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python

    # Make the str2 be the shortest string.
    if len(str1) < len(str2):
        return _levenshtein_distance(str2, str1)

    # Stop early in the event that the shortest string
    # doesn't even have anything in it.
    if len(str2) == 0:
        if -1 < max_distance < len(str2):
            return max_distance, False
        else:
            return len(str1), True

    previous_row: tp.List[int] = list(range(len(str2) + 1))
    for i, c1 in enumerate(str1):
        current_row: tp.List[int] = [i + 1]
        for j, c2 in enumerate(str2):
            # j+1 instead of j since previous_row and current_row are one character longer
            # than str2
            insertion_cost: int = previous_row[j + 1] + 1
            deletion_cost: int = current_row[j] + 1
            substitution_cost: int = previous_row[j] + (c1 != c2)
            current_row.append(min(insertion_cost, deletion_cost, substitution_cost))

        # replace previous row.
        previous_row = current_row

        # If we should be worrying about the distance, worry about it
        if max_distance > -1:
            # Only continue if all of our numbers are not greater than the max distance.
            should_continue: bool = any([n <= max_distance for n in previous_row])

            if not should_continue:
                return max_distance, False

    return previous_row[-1], True


_pattern_whitelists: tp.Dict[TurnipPattern, tp.Set[str]] = {
    TurnipPattern.DECREASING: {'decreasing', 'd'},
    TurnipPattern.HIGH_SPIKE: {'high spike', 'big spike', 'sudden spike', 'bs', 'ls'},
    TurnipPattern.SMALL_SPIKE: {'small spike', 'slow spike', 'gentle spike', 'ss', 'smol spike', 'gentle', 'small'},
    TurnipPattern.RANDOM: {'random', 'fluctuating', 'r', 'rd'}
}


def get_pattern(pattern_str: str, use_distance_metric: bool = True, max_distance: int = 4) -> TurnipPattern:
    """
    Uses a series of whitelists and the levenshtein distance metric to determine what type of pattern the input string is meant to be.
    This is because some users did not put in the actual value of the pattern and instead put something related to the pattern.
    An example is: Large Spike is the actual pattern, but the user put in BIIIIIG SPIKE.
    :param pattern_str: The possibly dirty pattern string that is in the raw data.
    :param use_distance_metric: If true (default), function will use distance metric in calculations. Won't otherwise.
    :param max_distance: The distance the distance metric will stop at if all values pass this. Default is 4 and won't be used if use_distance_metric is False.
    :return: The appropriate TurnipPattern for the input string, Empty if pattern_str is empty, or Unknown if it cannot be determined otherwise.
    """
    if len(pattern_str) == 0:
        return TurnipPattern.EMPTY

    in_str: str = pattern_str.lower()

    for k, v in _pattern_whitelists.items():
        if in_str in v:
            return k

    if use_distance_metric and len(in_str) >= max_distance:
        for k, v in _pattern_whitelists.items():
            # If any of the distances between the values and the in_str are within the maximum distance,
            # return the key.
            if any([_levenshtein_distance(val, in_str, max_distance=max_distance)[1] for val in v]):
                return k

    return TurnipPattern.UNKNOWN


def island_data_to_numpy(rows: tp.List[IslandWeekData], is_perfect: bool = False) -> np.ndarray:
    if is_perfect:
        return np.asarray([row.to_numpy() for row in rows if row.is_perfect()])
    else:
        return np.asarray([row.to_numpy() for row in rows if row.is_valid(MIN_NUM_PRICES)])


def island_data_get_current_patterns(rows: tp.List[IslandWeekData], is_perfect: bool = False) -> np.ndarray:
    if is_perfect:
        return np.asarray([[row.current_pattern.value[1]] for row in rows if row.is_perfect()])
    else:
        return np.asarray([[row.current_pattern.value[1]] for row in rows if row.is_valid(MIN_NUM_PRICES)])


def get_perfect_data(rows: tp.List[IslandWeekData]) -> tp.Tuple[np.ndarray, np.ndarray]:
    return island_data_to_numpy(rows, is_perfect=True), island_data_get_current_patterns(rows, is_perfect=True)


def get_all_data(rows: tp.List[IslandWeekData]) -> tp.Tuple[np.ndarray, np.ndarray]:
    return island_data_to_numpy(rows, is_perfect=False), island_data_get_current_patterns(rows, is_perfect=False)


def save_model(model_name: str, model) -> tp.Tuple[str, str]:
    date_str: str = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename: str = f'{model_name.replace(" ", "")}_{date_str}.mdl'
    file_path: str = os.path.join(MODEL_FILEPATH, filename)
    with open(file_path, 'wb') as f:
        pickle.dump(model, f)
    return file_path, filename


def load_model(filename: str):
    with open(os.path.join(MODEL_FILEPATH, filename), 'rb') as f:
        return pickle.load(f)


def get_max_cv(y: np.ndarray) -> int:
    return min(np.unique(y, return_counts=True)[1])


def populate_current_pattern(rows: tp.List[IslandWeekData], best_classifier) -> tp.List[IslandWeekData]:
    return [row.predict_current_pattern(best_classifier) if not row.has_patterns_populated() else row for row in rows]
