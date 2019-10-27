import math


def round_half_up(n, decimals=0):
    """
    Applys half-up rounding to the given float
    ---
    Params:
        n: float, the number to half-up round
        decimals: int, the number of decimals to round up to
    Returns:
        float, the half-up rounded result
    """
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier
