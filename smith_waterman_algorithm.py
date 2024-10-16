import numpy as np
import pandas as pd

def smith_waterman(seq1, seq2):
    # Scoring parameters
    match_score, mismatch_score, gap_penalty = 5, -3, -4

    # Initialize the scoring matrix
    len_m, len_n = len(seq1), len(seq2)
    scoring_matrix = [[0 for j in range(len_m + 1)] for i in range(len_n + 1)]                                       

    # Keep track of the maximum score and its position for traceback
    max_score = 0
    max_pos = (0, 0)

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
            scoring_matrix[i][j] = max(match, delete, insert, 0)
            if scoring_matrix[i][j] > max_score:
                max_score = scoring_matrix[i][j]
                max_pos = (i, j)

    # Traceback to build the alignment
    aligned_seq1 = ""
    aligned_seq2 = ""
    i, j = max_pos

    while i > 0 and j > 0 and scoring_matrix[i][j] != 0:
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

    return aligned_seq1, aligned_seq2, scoring_matrix, max_score

seq1 = "GAATTCAGTTA"
seq2 = "GGATCGA"
aligned_seq1, aligned_seq2, scoring_matrix, alignment_score = smith_waterman(seq1, seq2)
print(f"Sequence 1: {aligned_seq1}")
print(f"Sequence 2: {aligned_seq2}")
# for row in scoring_matrix:
#      print (row)
# print(*scoring_matrix, sep = '\n')
print(np.matrix(scoring_matrix))
print(f"Optimal Alignment Score: {alignment_score}")

# Sequence 1: GAATTCAG
# Sequence 2: GGA-TC-G
# [[ 0  0  0  0  0  0  0  0  0  0  0  0]
#  [ 0  5  1  0  0  0  0  0  5  1  0  0]
#  [ 0  5  2  0  0  0  0  0  5  2  0  0]
#  [ 0  1 10  7  3  0  0  5  1  2  0  5]
#  [ 0  0  6  7 12  8  4  1  2  6  7  3]
#  [ 0  0  2  3  8  9 13  9  5  2  3  4]
#  [ 0  5  1  0  4  5  9 10 14 10  6  2]
#  [ 0  1 10  6  2  1  5 14 10 11  7 11]]                                  
# Optimal Alignment Score: 14
