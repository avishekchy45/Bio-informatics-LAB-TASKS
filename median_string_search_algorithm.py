import itertools

def hamming_distance(s1, s2):
    distance = sum(c1 != c2 for c1, c2 in zip(s1, s2))                                                   
    return distance                                                                    

def distance_to_closest_pattern(pattern, sequence):
    min_distance = float('inf')
    for i in range(len(sequence) - l + 1):
        substring = sequence[i:i + l]
        distance = hamming_distance(pattern, substring)
        if distance < min_distance:
            min_distance = distance
    return min_distance                                                                                    

def median_string_search(dna_sequences, l):
    alphabet = ['A', 'C', 'G', 'T']

    # Generate all possible strings of length l
    all_possible_strings = [''.join(p) for p in itertools.product(alphabet, repeat=l)]

    # Initialize variables to track the best median string
    best_median_string = None
    best_total_distance = float('inf')

    # For each possible string, calculate the total distance to all sequences
    for pattern in all_possible_strings:
        total_distance = 0
        for sequence in dna_sequences:
            total_distance += distance_to_closest_pattern(pattern, sequence)

        # If we found a smaller total distance, update the best median string
        if total_distance < best_total_distance:
            best_total_distance = total_distance
            best_median_string = pattern

    return best_median_string                                                                               

dna_sequences = [
    "AGCTGACCTG",
    "CGCTGACGTA",
    "GCTGACCTGA",
    "TCTGACGTCA"
]
l = 3  # Length of the median string
median_string = median_string_search(dna_sequences, l)
print(f"Median String: {median_string}")

# Median String: CTG                                                                 
