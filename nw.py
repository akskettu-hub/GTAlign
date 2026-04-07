import Levenshtein


# LLM Generated
def word_cost(w1, w2):
    return Levenshtein.distance(w1, w2) / max(len(w1), len(w2))


# LLM Generated. Implements Needleman–Wunsch alignment
def align_words(seq1: list[tuple], seq2: list[str]):

    n, m = len(seq1), len(seq2)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    gap_cost = 1

    for i in range(1, n + 1):
        dp[i][0] = i * gap_cost

    for j in range(1, m + 1):
        dp[0][j] = j * gap_cost

    for i in range(1, n + 1):
        for j in range(1, m + 1):

            sub_cost = word_cost(seq1[i - 1][1], seq2[j - 1])

            dp[i][j] = min(
                dp[i - 1][j] + gap_cost,
                dp[i][j - 1] + gap_cost,
                dp[i - 1][j - 1] + sub_cost,
            )

    # backtrack

    i, j = n, m
    alignment = []

    while i > 0 or j > 0:

        if i > 0 and dp[i][j] == dp[i - 1][j] + gap_cost:
            alignment.append((seq1[i - 1][0], seq1[i - 1][1], None))
            i -= 1

        elif j > 0 and dp[i][j] == dp[i][j - 1] + gap_cost:
            alignment.append((None, None, seq2[j - 1]))
            j -= 1

        else:
            alignment.append((seq1[i - 1][0], seq1[i - 1][1], seq2[j - 1]))
            i -= 1
            j -= 1

    alignment.reverse()

    return alignment
