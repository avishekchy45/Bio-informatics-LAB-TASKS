from collections import Counter

def remove_distances(D, distances):
    D_count = Counter(D)  # Multiset behavior using Counter
    for d in distances:
        if D_count[d] > 0:
            D_count[d] -= 1
        else:
            return None  # If we can't remove the required distance, return None
    return list(D_count.elements())  # Return the remaining multiset as a list                                         

def place_point(D, positions, L):
    if not D:
        return positions  # If D is empty, we've placed all points correctly

    max_dist = max(D)  # The largest remaining distance in D

    # Try placing a new point at max_dist from 0 (right side placement)
    possible_point = max_dist
    new_distances = [abs(possible_point - p) for p in positions]
    new_D = remove_distances(D, new_distances)

    if new_D is not None:
        positions.append(possible_point)
        result = place_point(new_D, positions, L)
        if result:
            return result
        positions.pop()  # Backtrack if placing at max_dist didn't work

    # Try placing the new point at L - max_dist (left side placement)
    possible_point = L - max_dist
    new_distances = [abs(possible_point - p) for p in positions]
    new_D = remove_distances(D, new_distances)

    if new_D is not None:
        positions.append(possible_point)
        result = place_point(new_D, positions, L)
        if result:
            return result
        positions.pop()  # Backtrack if placing at L - max_dist didn't work

    return None  # If neither placement worked, return None                                                             

def partial_digest(D):
    L = max(D)  # The largest distance corresponds to the distance between the outermost points
    D.remove(L)  # Remove L from the multiset
    positions = [0, L]  # Place points at 0 and L

    # Start the recursive placement
    result = place_point(D, positions, L)

    return sorted(result) if result else None                                                                             

D = [2, 2, 3, 3, 4, 5, 6, 7, 8, 10]
positions = partial_digest(D)
print(f"Positions: {positions}")

# Positions: [0, 3, 6, 8, 10]                                                              
