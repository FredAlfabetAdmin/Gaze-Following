# Congruent vs Incongruent
# FO-GO
# Primary and Secondary

import itertools
import random
def create_random_trials():
    items = ['speech', 'visual', 'gesture']
    combinations = list(itertools.combinations(items, 2))
    trials = []
    for combination in combinations:
        for x in range(2): # Primary and Secondary
            for y in range(2): # Congruent and Incongruent
                for z in range(2): # Direction
                    trials.append({
                        'first_item':combination[0],
                        'second_item':combination[1],
                        'primary': combination[0] if x == 0 else combination[1],
                        'congruent': y == 0,
                        'direction': 'left' if z == 0 else 'right'
                    })

    return random.shuffle(trials)
