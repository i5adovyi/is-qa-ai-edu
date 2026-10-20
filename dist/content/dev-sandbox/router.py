"""Deliberately buggy lesson fixture. Copy to work/ before repairing it.

This file is NOT used by the reference lab. Its public contract permits at
most max_steps successful calls and raises RuntimeError thereafter.
"""

def take_step(used, max_steps):
    """Return the next consumed-step count, or raise when budget is exhausted."""
    if type(used) is not int or type(max_steps) is not int:
        raise ValueError('Budgets must be integers, not booleans.')
    if used < 0 or max_steps < 0:
        raise ValueError('Budgets cannot be negative.')
    # Intentional exercise defect: an exhausted budget should reject dispatch.
    if used <= max_steps:
        return used + 1
    raise RuntimeError('Step budget exhausted.')
