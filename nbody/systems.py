"""Preset initial conditions for common test systems."""
import numpy as np
from .body import Body


def two_body(G: float = 1.0) -> list[Body]:
    """Two equal masses in a circular orbit about their common center of mass.

    Uses normalized units where G = 1, total mass = 2, separation = 1.
    For a circular orbit of two equal masses m at separation r:
        orbital speed v = sqrt(G * m / (2 * r))  (relative to COM)

    Returns a list of two Body objects whose center of mass is at the origin
    and whose total momentum is zero.
    """
    m = 1.0
    r = 0.5  # each body sits at distance r from the COM, so separation = 2r = 1
    # Speed for circular orbit about the COM
    v = np.sqrt(G * m / (4 * r))

    body1 = Body(
        mass=m,
        position=np.array([r, 0.0]),
        velocity=np.array([0.0, v]),
    )
    body2 = Body(
        mass=m,
        position=np.array([-r, 0.0]),
        velocity=np.array([0.0, -v]),
    )
    return [body1, body2]