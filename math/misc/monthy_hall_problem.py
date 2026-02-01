"""
Monty Hall problem

In the Monty Hall problem, you pick one of three doors. One hides a car and the two 
other hide goats. After your choice, Monty opens a goat door. You should switch. 
Switching doubles your winning odds from 1/3 to 2/3.
"""

import random

# some consts
N_LOOPS = 100_000
N_GATES = 3


# some functions
def init_gates(n: int) -> list:
    """ Init 3 gates with only one is True. """
    gates = [False] * n
    gates[random.randrange(n)] = True
    return gates


def gates_choice(gates: list, skip_gates: list | None = None) -> int:
    """ choice a gate between all available. """
    # default args
    if skip_gates is None:
        skip_gates = []
    # check args consistency
    if len(gates) <= len(skip_gates):
        raise ValueError('all gates are skipped')
    # filter indices
    available_indices = [i for i in range(len(gates)) if i not in skip_gates]
    return random.choice(available_indices)


# init vars
wins_stay = 0
wins_switch = 0

# game loop
for _ in range(N_LOOPS):
    # init gates
    gates = init_gates(N_GATES)
    # first canditate choice (randomly pick a gate)
    first_choice = gates_choice(gates)
    # monty choice is never the first candidate choice (here first_choice) and never the only True gate
    monty_choice = None
    for i in range(len(gates)):
        # skip first choice
        if i == first_choice:
            continue
        # find the first False value
        if not gates[i]:
            monty_choice = i
            break
    assert monty_choice is not None, 'unable to find a Monty choice'
    # second canditate choice
    second_choice = gates_choice(gates, skip_gates=[first_choice, monty_choice])
    # record results
    if gates[first_choice]:
        wins_stay += 1
    if gates[second_choice]:
        wins_switch += 1

# results calculation
ratio_stay = wins_stay / N_LOOPS
ratio_switch = wins_switch / N_LOOPS

print(f'staying wins   : {wins_stay:>9_} (p={ratio_stay:.3f})')
print(f'switching wins : {wins_switch:>9_} (p={ratio_switch:.3f})')
