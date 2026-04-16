# Summary from LMU explanation for N-body simulations

## Tree Struct

The easiest and initially most intuitive way is the so called direct summation approach (brute force). The force exerted on a particle i is the sum of the forces from all other particles *"j not equal to i"* inside the system.

This technique gives the correct acceleration for every particle.

**Operations required :** O(N2).

For simulations of collisionless systems, a small error in the accelerations is tolerable. Feasible to implement methods which require less than O(N2) operations while producing slightly less accurate accelerations for the particles.

**Most common method :** ordering the particles into a tree structure.
Instead of computing every interaction with a remote set of particles, a single interaction with a node of the tree structure is computed, where the node contains a corresponding set of particles. Two such variants are the *"octree"* and *"binary tree"* structures.

**Operations required :** O(N log N)

### Octree

Tree is built top down. The system is placed into a cube encompassing all particles. The cube is split into its eight octants, which are then in turn split accordingly. Repeat until one or no particle inside cube.

### Binary Tree

Built bottom up. Nearest neighbour particles into nodes of tree until root node is left. Naturally follows geometry of physical system.

## Relaxation and stability of N-body simulations

To evaluate gravitational force, use formula as is, with $\epsilon$ being included as : (|x~i~ - x~j~|^2 + $\epsilon$^2)^3/2 in the denominator, as a softener to avoid divergence at i = j.

Newtons equations for motion are : v = dx/dt , F = mdv/dt

To integrate this set of equations numerically it is necessary to replace them by linear algebraic relationships. The continuous functions x and v are replaced by values at discrete time intervals. The most commonly used discretization for N-body simulations is the leapfrog scheme or Verlet method - the standard method of integrating equations of motion for interacting particles where interactions arent explicitly dependent on velocity, eg. stellar dynamics.
