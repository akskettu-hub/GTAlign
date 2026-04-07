import Levenshtein
from nltk import word_tokenize


def word_tokenize_text(text: str):
    tokenized_text = word_tokenize(text, language="english")

    return tokenized_text


# LLM Generated
def word_cost(w1, w2):
    return Levenshtein.distance(w1, w2) / max(len(w1), len(w2))


# LLM Generated. Implements Needleman–Wunsch alignment
def align_words(seq1: list[tuple], seq2: list[str]):

    n, m = len(seq1), len(seq2)

    # construct a matrix of dimensions n + 1 x m + 1
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # The cost of an insertion or deletion = 1
    gap_cost = 1

    # for each row, inset i*gap_cost to the zeroeth element
    for i in range(1, n + 1):
        dp[i][0] = i * gap_cost

    # for the top column fill each element with i*gap_cost
    for j in range(1, m + 1):
        dp[0][j] = j * gap_cost

    # i = row, j = column, starting at 1,1 and moving by column and then row, assign value to each comparrison
    for i in range(1, n + 1):
        for j in range(1, m + 1):

            sub_cost = word_cost(seq1[i - 1][1], seq2[j - 1])

            # assign to the cell in question the lowest value of:
            # cell to the top of current, cell to the left, cell to the top left
            # add gap cost to result except for top left, which gets the substitution cost
            dp[i][j] = min(
                dp[i - 1][j] + gap_cost,
                dp[i][j - 1] + gap_cost,
                dp[i - 1][j - 1] + sub_cost,
            )

    # backtrack

    # set i, j to lower right of the matrix
    i, j = n, m
    alignment = []

    # While at least 1 index is not zero
    while i > 0 or j > 0:

        # if i still has stuff in it
        #
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


if __name__ == "__main__":
    a = "This is some very long sentence I love lamp"
    b = "This is sentencek I love lamp"
    a = "I'd already told him"
    b = "Id already told him"
    a = word_tokenize(a)
    b = word_tokenize(b)

    res = align_words(a, b)
    print(res)
