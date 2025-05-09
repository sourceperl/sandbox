def arange(start, stop=None, step: float = 1.0, inclusive: bool = False):
    """
    Generate a sequence of numbers similar to numpy.arange.

    This function generates a list of numbers starting from `start` to `stop` (exclusive),
    incremented by `step`. It supports both positive and negative step values and can optionally
    include the `stop` value if it matches exactly.

    Parameters:
    - start (float): The starting value of the sequence.
    - stop (float, optional): The end value of the sequence (exclusive). If not provided, `start` is treated as `stop` 
    and `start` is set to 0.
    - step (float, optional): The increment (or decrement) between each number in the sequence. Default is 1.0.
    - inclusive (bool, optional): If True, the sequence will include the `stop` value if it matches exactly. Default 
    is False.

    Returns:
    - list: A list of numbers in the sequence.

    Raises:
    - ValueError: If `step` is zero.

    Examples:
    >>> arange(0, 10, 0.1)
    [0, 0.1, 0.2, ..., 9.9]

    >>> arange(5)
    [0, 1, 2, 3, 4]

    >>> arange(10, 0, -1)
    [10, 9, 8, ..., 1]
    """

    if stop is None:
        stop = start
        start = 0.0

    if step == 0:
        raise ValueError("Step cannot be zero.")

    # Determine the direction of the step
    if step > 0:
        # For positive step
        num_steps = int((stop - start) / step)
        epsilon = 1e-10  # Small value to handle floating-point precision
        if inclusive and abs(start + num_steps * step - stop) < epsilon:
            num_steps += 1
    else:
        # For negative step
        num_steps = int((start - stop) / (-step))
        epsilon = 1e-10  # Small value to handle floating-point precision
        if inclusive and abs(start + num_steps * step - stop) < epsilon:
            num_steps += 1

    return [start + i * step for i in range(num_steps)]
