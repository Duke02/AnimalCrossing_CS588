"""
Utility file to help determine different aspects about the data.
"""
import typing as tp

from island_week_data import TurnipPattern


def _levenshtein_distance(str1: str, str2: str, max_distance: int = -1) -> tp.Tuple[int, bool]:
    """
    My favorite distance metric for strings. Calculates the number of substitutions, deletions, and additions must be
    made to str1 in order for it to be made into str2.
    :param str1: The first string to compare.
    :param str2: The second string to compare.
    :param max_distance: The function will stop if the distance is over the max_distance. If equal to -1 (the default), the function won't stop early.
    :return: A tuple containing the resulting distance and whether the function was able to fully calculate the metric.
    """
    if str1 == str2:
        return 0, True

    vector1: tp.List[int] = [i for i in range(len(str1))]
    vector2: tp.List[int] = [0 for _ in range(len(str2))]

    for i in range(len(str2)):
        vector2[0] = i + 1

        for j in range(len(str1)):
            deletion_cost: int = vector1[j + 1]
            insertion_cost: int = vector2[j] + 1

            substitution_cost: int = vector1[j]

            if str1[i] != str2[j]:
                substitution_cost += 1

            vector2[j + 1] = min(deletion_cost, insertion_cost, substitution_cost)

        temp: tp.List[int] = vector1[:]
        vector1 = vector2[:]
        vector2 = temp[:]

        if max_distance > -1:
            should_stop: bool = all([n >= max_distance for n in vector1 + vector2])

            if should_stop:
                return max_distance, False

    return vector1[-1], True


_pattern_whitelists: tp.Dict[TurnipPattern, tp.Set[str]] = {
    TurnipPattern.DECREASING: {'decreasing'},
    TurnipPattern.HIGH_SPIKE: {'high spike', 'big spike', 'sudden spike'},
    TurnipPattern.SMALL_SPIKE: {'small spike', 'slow spike'},
    TurnipPattern.RANDOM: {'random'}
}


def get_pattern(pattern_str: str, use_distance_metric: bool = True, max_distance: int = 4) -> TurnipPattern:
    """
    Uses a series of whitelists and the levenshtein distance metric to determine what type of pattern the input string is meant to be.
    This is because some users did not put in the actual value of the pattern and instead put something related to the pattern.
    An example is: Large Spike is the actual pattern, but the user put in BIIIIIG SPIKE.
    :param pattern_str: The possibly dirty pattern string that is in the raw data.
    :param use_distance_metric: If true (default), function will use distance metric in calculations. Won't otherwise.
    :param max_distance: The distance the distance metric will stop at if all values pass this. Default is 4 and won't be used if use_distance_metric is False.
    :return: The appropriate TurnipPattern for the input string, or Unknown if it cannot be determined.
    """
    in_str: str = pattern_str.lower()

    for k, v in _pattern_whitelists:
        if in_str in v:
            return k

    if use_distance_metric:
        for k, v in _pattern_whitelists:
            # If any of the distances between the values and the in_str are within the maximum distance,
            # return the key.
            if any([_levenshtein_distance(val, in_str, max_distance=max_distance)[1] for val in v]):
                return k

    return TurnipPattern.UNKNOWN
