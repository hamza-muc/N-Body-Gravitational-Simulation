"""Direct O(N^2) gravitational force calculation, vectorized with NumPy."""
import numpy as np
from ..body import Body


def compute_accelerations(
    bodies: list[Body],
    G: float = 1.0,
    softening: float = 1e-3,
) -> np.ndarray:
    """Compute gravitational acceleration on each body from all others.

    Uses direct pairwise summation: O(N^2) in the number of bodies.
    Vectorized with NumPy broadcasting — no Python loops over body pairs.

    Args:
        bodies: List of Body objects.
        G: Gravitational constant (1.0 in normalized units).
        softening: Small length added to the denominator to prevent the
            1/r^2 force from diverging when two bodies pass very close.
            Without this, close encounters produce numerical explosions.

    Returns:
        An (N, D) array of accelerations, where N is the number of bodies
        and D is the spatial dimension (2 or 3).
    """
    # Stack positions and masses into arrays for vectorized math.
    positions = np.array([b.position for b in bodies])   # shape (N, D)
    masses = np.array([b.mass for b in bodies])          # shape (N,)

    # Pairwise displacement vectors: r_ij = r_j - r_i
    # positions[np.newaxis, :, :] has shape (1, N, D)
    # positions[:, np.newaxis, :] has shape (N, 1, D)
    # Broadcasting subtracts them to give shape (N, N, D)
    # where displacements[i, j] = position of j minus position of i.
    displacements = positions[np.newaxis, :, :] - positions[:, np.newaxis, :]

    # Squared distances with softening, shape (N, N)
    dist_squared = np.sum(displacements ** 2, axis=-1) + softening ** 2

    # Inverse cube of distance, shape (N, N)
    # Gravitational acceleration on i from j is: G * m_j * (r_j - r_i) / |r_ij|^3
    inv_dist_cubed = dist_squared ** (-1.5)

    # Zero out self-interaction (i == j): a body exerts no force on itself.
    # Without this, dist_squared[i,i] = softening^2, giving a spurious self-force.
    np.fill_diagonal(inv_dist_cubed, 0.0)

    # Acceleration on body i = G * sum over j of  m_j * (r_j - r_i) / |r_ij|^3
    # displacements has shape (N, N, D); inv_dist_cubed[:, :, None] broadcasts
    # to (N, N, 1); masses[None, :, None] broadcasts to (1, N, 1).
    # Sum over the j axis (axis=1) to get shape (N, D).
    accelerations = G * np.sum(
        masses[np.newaxis, :, np.newaxis]
        * displacements
        * inv_dist_cubed[:, :, np.newaxis],
        axis=1,
    )

    return accelerations