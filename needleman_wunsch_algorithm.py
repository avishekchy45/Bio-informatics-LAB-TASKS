import numpy as np
import pandas as pd

def needleman_wunsch(seq1, seq2):
    # Scoring parameters
    match_score, mismatch_score, gap_penalty = 5, -3, -4

    # Initialize the scoring matrix
    len_m, len_n = len(seq1), len(seq2)
    scoring_matrix = [[0 for j in range(len_m + 1)] for i in range(len_n + 1)]                                       

    # Initialize the first row and column with gap penalties
    for i in range(1, len_n + 1):
        scoring_matrix[i][0] = i * gap_penalty
    for j in range(1, len_m + 1):
        scoring_matrix[0][j] = j * gap_penalty

    # Fill in the scoring matrix
    for i in range(1, len_n + 1):
        for j in range(1, len_m + 1):
            # print(i, j)
            if seq2[i - 1] == seq1[j - 1]:
                match = scoring_matrix[i - 1][j - 1] + match_score
            else:
                match = scoring_matrix[i - 1][j - 1] + mismatch_score
            delete = scoring_matrix[i - 1][j] + gap_penalty
            insert = scoring_matrix[i][j - 1] + gap_penalty
            scoring_matrix[i][j] = max(match, delete, insert)

    alignment_score = scoring_matrix[len_n][len_m]

    # Traceback to build the alignment
    aligned_seq1 = ""
    aligned_seq2 = ""
    i, j = len_n, len_m

    while i > 0 and j > 0:
        current_score = scoring_matrix[i][j]
        diagonal_score = scoring_matrix[i - 1][j - 1]
        up_score = scoring_matrix[i - 1][j]
        left_score = scoring_matrix[i][j - 1]

        # Check if diagonal (match or mismatch)
        if seq2[i - 1] == seq1[j - 1]:
            score = match_score
        else:
            score = mismatch_score

        if current_score == diagonal_score + score:
            aligned_seq2 = seq2[i - 1] + aligned_seq2
            aligned_seq1 = seq1[j - 1] + aligned_seq1
            i -= 1
            j -= 1
        elif current_score == up_score + gap_penalty:
            aligned_seq2 = seq2[i - 1] + aligned_seq2
            aligned_seq1 = "-" + aligned_seq1
            i -= 1
        else:  # current_score == left_score + gap_penalty
            aligned_seq2 = "-" + aligned_seq2
            aligned_seq1 = seq1[j - 1] + aligned_seq1
            j -= 1

    # If one sequence is longer, add gaps to the shorter sequence
    while i > 0:
        aligned_seq2 = seq2[i - 1] + aligned_seq2
        aligned_seq1 = "-" + aligned_seq1
        i -= 1
    while j > 0:
        aligned_seq2 = "-" + aligned_seq2
        aligned_seq1 = seq1[j - 1] + aligned_seq1
        j -= 1

    return aligned_seq1, aligned_seq2, scoring_matrix, alignment_score

seq1 = "GAATTCAGTTA"
seq2 = "GGATCGA"
aligned_seq1, aligned_seq2, scoring_matrix, alignment_score = needleman_wunsch(seq1, seq2)
print(f"Sequence 1: {aligned_seq1}")
print(f"Sequence 2: {aligned_seq2}")
# for row in scoring_matrix:
#      print (row)
# print(*scoring_matrix, sep = '\n')
print(np.matrix(scoring_matrix))
print(f"Optimal Alignment Score: {alignment_score}")

# Sequence 1: GAATTCAGTTA
# Sequence 2: GGA-TC-G--A
# [[  0  -4  -8 -12 -16 -20 -24 -28 -32 -36 -40 -44] 
#  [ -4   5   1  -3  -7 -11 -15 -19 -23 -27 -31 -35] 
#  [ -8   1   2  -2  -6 -10 -14 -18 -14 -18 -22 -26] 
#  [-12  -3   6   7   3  -1  -5  -9 -13 -17 -21 -17] 
#  [-16  -7   2   3  12   8   4   0  -4  -8 -12 -16] 
#  [-20 -11  -2  -1   8   9  13   9   5   1  -3  -7] 
#  [-24 -15  -6  -5   4   5   9  10  14  10   6   2] 
#  [-28 -19 -10  -1   0   1   5  14  10  11   7  11]]                                
# Optimal Alignment Score: 11
