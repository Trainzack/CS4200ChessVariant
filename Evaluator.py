from MatchRunner import MatchData

def evaluate(data: MatchData) -> float:
    """

    :param data: The matchData containing the matches that we want to evaluate
    :return: A float representing how fit the variant is, currently based on W/L/D rate
    """

    whiteWins = data.whiteWins
    blackWins = data.blackWins
    draws = data.draws

    evaluation = winLossDrawEvaluation(whiteWins, blackWins, draws)

    return evaluation


def winLossDrawEvaluation(wins: int, losses: int, draws: int) -> float:

    drawRatio = draws/(wins + losses + draws)
    halfDraws = draws/2
    winRatio = 0

    # The win Ratio is the ratio between times the side that tends to lose loses and does not loose.
    # If both are equal, then ratio is 1. If both sides never win, then the ratio is 0.

    if wins > losses:
        winRatio = (losses + halfDraws) / (wins + halfDraws)
    elif losses > wins:
        winRatio = (wins + halfDraws) / (losses + halfDraws)
    elif losses != 0 and wins != 0:
        winRatio = 1
    else:
        winRatio = 0

    return (20.0 * winRatio ** 0.4) - (5.0 * drawRatio ** 0.4)