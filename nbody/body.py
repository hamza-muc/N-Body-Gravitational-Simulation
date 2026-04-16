"""Body: a point mass with position and velocity."""
from dataclasses import dataclass
import numpy as np


@dataclass
class Body:
    """A point mass in the simulation.

    Attributes:
        mass: Scalar mass of the body.
        position: Position vector as a NumPy array. Length 2 for 2D, 3 for 3D.
        velocity: Velocity vector as a NumPy array. Same length as position.
    """
    mass: float
    position: np.ndarray
    velocity: np.ndarray

    def __post_init__(self):
        # Ensure arrays are float (so in-place updates don't truncate to int)
        # and that position and velocity have matching shapes.
        self.position = np.asarray(self.position, dtype=float)
        self.velocity = np.asarray(self.velocity, dtype=float)
        if self.position.shape != self.velocity.shape:
            raise ValueError(
                f"position shape {self.position.shape} != "
                f"velocity shape {self.velocity.shape}"
            )