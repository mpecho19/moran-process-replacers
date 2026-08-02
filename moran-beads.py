import numpy as np
from typing import Sequence


# Vertex order used by the binary index:
# index = 32*a + 16*b + 8*c + 4*d + 2*e + f
VERTICES = ("a", "b", "c", "d", "e", "f")

A, B, C, D, E, F = range(6)

NEIGHBORS = {
    A: (B, C, D),
    B: (A, C, D, E),
    C: (A, B, D, E),
    D: (A, B, C, E),
    E: (B, C, D, F),
    F: (E,),
}


def state_to_index(state: Sequence[int]) -> int:
    """
    Convert (a,b,c,d,e,f) to the binary index

        32*a + 16*b + 8*c + 4*d + 2*e + f.

    Here 1 means mutant and 0 means residents.
    """
    if len(state) != 6 or any(x not in (0, 1) for x in state):
        raise ValueError("A state must be a length-6 sequence of zeros and ones.")

    return sum(bit << (5 - i) for i, bit in enumerate(state))


def index_to_state(index: int) -> tuple[int, ...]:
    """
    Convert an integer from 0 to 63 to the state (a,b,c,d,e,f).
    """
    if not 0 <= index < 64:
        raise ValueError("The state index must lie between 0 and 63.")

    return tuple((index >> (5 - i)) & 1 for i in range(6))


def is_failure(state: Sequence[int]) -> bool:
    """Failure occurs when a is a resident."""
    return state[A] == 0


def is_success(state: Sequence[int]) -> bool:
    """Success occurs when all of a,b,c,d,e are mutants."""
    return all(state[v] == 1 for v in (A, B, C, D, E))


def is_terminal(state: Sequence[int]) -> bool:
    return is_failure(state) or is_success(state)


def transition_probabilities_from_state(
    state: Sequence[int],
    r: float,
) -> np.ndarray:
    """
    Return an array p of length 64, where p[j] is the transition
    probability from `state` to the state with binary index j.
    """
    if r <= 0:
        raise ValueError("The fitness parameter r must be positive.")

    state = tuple(state)

    if len(state) != 6 or any(x not in (0, 1) for x in state):
        raise ValueError("A state must be a length-6 sequence of zeros and ones.")

    probabilities = np.zeros(64, dtype=float)
    current_index = state_to_index(state)

    # The stopped process makes success and failure states absorbing.
    if is_terminal(state):
        probabilities[current_index] = 1.0
        return probabilities

    fitness = np.array(
        [r if state[v] == 1 else 1.0 for v in range(6)],
        dtype=float,
    )
    total_fitness = fitness.sum()

    for reproducer in range(6):
        reproducer_probability = fitness[reproducer] / total_fitness

        opposite_neighbors = [
            neighbor
            for neighbor in NEIGHBORS[reproducer]
            if state[neighbor] != state[reproducer]
        ]

        # No opposite-colored neighbor: self-loop.
        if not opposite_neighbors:
            probabilities[current_index] += reproducer_probability
            continue

        neighbor_probability = 1.0 / len(opposite_neighbors)

        for target in opposite_neighbors:
            attempt_probability = reproducer_probability * neighbor_probability

            # Exceptional failed transition:
            # mutant e attempts to recolor resident f.
            if (
                reproducer == E
                and target == F
                and state[E] == 1
                and state[F] == 0
            ):
                probabilities[current_index] += attempt_probability
                continue

            new_state = list(state)
            new_state[target] = state[reproducer]
            new_index = state_to_index(new_state)

            probabilities[new_index] += attempt_probability

    return probabilities


def transition_matrix(r: float) -> np.ndarray:
    """
    Construct the full 64 x 64 transition matrix P.

    P[i, j] is the probability of moving from state i to state j.
    """
    P = np.zeros((64, 64), dtype=float)

    for i in range(64):
        state = index_to_state(i)
        P[i, :] = transition_probabilities_from_state(state, r)

    return P



def success_probability_by_state(r: float) -> np.ndarray:
    """
    Compute the probability of reaching success before failure
    from every one of the 64 states.

    Returns
    -------
    u : np.ndarray
        u[i] is the success probability starting from state index i.
    """
    P = transition_matrix(r)

    success_indices = []
    failure_indices = []
    transient_indices = []

    for i in range(64):
        state = index_to_state(i)

        if is_success(state):
            success_indices.append(i)
        elif is_failure(state):
            failure_indices.append(i)
        else:
            transient_indices.append(i)

    u = np.zeros(64, dtype=float)
    u[success_indices] = 1.0


    Q = P[np.ix_(transient_indices, transient_indices)]
    P_to_success = P[np.ix_(transient_indices, success_indices)]

    right_hand_side = P_to_success.sum(axis=1)
    u_transient = np.linalg.solve(
        np.eye(len(transient_indices)) - Q,
        right_hand_side,
    )

    u[transient_indices] = u_transient

    return u


def initial_success_probability(r: float) -> float:
    """
    Probability of success starting from the initial state 100000.
    """
    initial_state = (1, 0, 0, 0, 0, 0)
    initial_index = state_to_index(initial_state)  # equals 32

    u = success_probability_by_state(r)
    return float(u[initial_index])


def compare_probabilities(r: float) -> tuple[float, float]:
    """
    Return:
      1. success probability from 100000;
      2. failure probability from 111100.
    """
    u = success_probability_by_state(r)

    initial_state = (1, 0, 0, 0, 0, 0)  # index 32
    near_success_state = (1, 1, 1, 1, 0, 0)  # index 60

    success_from_initial = float(u[state_to_index(initial_state)])
    failure_from_near_success = 1.0 - float(
        u[state_to_index(near_success_state)]
    )

    return success_from_initial, failure_from_near_success


if __name__ == "__main__":
    r_values = (1.01, 1.05, 1.08, 1.1, 1.2, 1.8)

    print(
        f"{'r':>8} "
        f"{'success from 100000':>24} "
        f"{'failure from 111100':>24}"
    )
    print("-" * 60)

    for r in r_values:
        success_probability, failure_probability = compare_probabilities(r)

        print(
            f"{r:8.2f} "
            f"{success_probability:24.12f} "
            f"{failure_probability:24.12f}"
        )

