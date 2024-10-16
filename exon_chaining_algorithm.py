def exon_chaining(intervals):
    # Step 1: Sort intervals by their end points
    intervals.sort(key=lambda x: x[1])

    # Number of intervals
    n = len(intervals)

    # dp[i] will store the maximum score up to interval i
    dp = [0] * n
    # To reconstruct the solution, store the previous index
    previous = [-1] * n

    # Helper function to find the rightmost non-overlapping interval
    def find_previous(intervals, i):
        for j in range(i - 1, -1, -1):
            if intervals[j][1] <= intervals[i][0]:
                return j
        return -1

    # Step 2: Fill the dp array
    for i in range(n):
        # Option 1: Exclude the current interval, take the best score up to i-1
        dp[i] = dp[i - 1] if i > 0 else 0

        # Option 2: Include the current interval
        previous_idx = find_previous(intervals, i)
        score_with_current = intervals[i][2]  # Score of the current interval

        if previous_idx != -1:
            score_with_current += dp[previous_idx]

        # Take the maximum of excluding or including the current interval
        dp[i] = max(dp[i], score_with_current)

        # Keep track of the best option
        if dp[i] == score_with_current:
            previous[i] = previous_idx

    # Step 3: Backtrack to find the optimal set of intervals
    result = []
    i = n - 1
    while i >= 0:
        if previous[i] != -1 or dp[i] > (dp[i - 1] if i > 0 else 0):
            result.append(intervals[i])
            i = previous[i]
        else:
            i -= 1

    return result[::-1]  # Return the intervals in sorted order                                                          

intervals = [ # (start, end, score)
    (1, 5, 5),
    (2, 3, 3),
    (4, 8, 6),
    (6, 12, 10),
    (7, 17, 12),
    (9, 10, 1),
    (11, 15, 7),
    (13, 14, 0),
    (16, 18, 4)
]
optimal_exons = exon_chaining(intervals)
print(f"Optimal set of exons: {optimal_exons}")

# Optimal set of exons: [(2, 3, 3), (4, 8, 6), (9, 10, 1), (11, 15, 7), (16, 18, 4)]                                   
