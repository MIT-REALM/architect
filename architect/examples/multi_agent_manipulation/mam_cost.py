from typing import Tuple

import jax.numpy as jnp

from .mam_simulator import mam_simulate_single_push_two_turtles


def mam_cost_push_two_turtles(
    design_params: jnp.ndarray,
    exogenous_sample: jnp.ndarray,
    layer_widths: Tuple[int],
    dt: float,
) -> jnp.ndarray:
    """Compute the cost based on given beacon locations.

    args:
        design_params: a (2 + n_beacons * 2) array of design parameters. The first two
                       entries are the controller gains and the rest are the beacon
                       locations when reshaped to (n_beacons, 2)
        exogenous_sample: (2 + T * (3 + n_beacons + 1)) array containing all randomness
                          used for the observation, actuation, and initial state noise.
                          Can be generated by AGVExogenousParameters.sample
        layer_widths: number of units in each layer. First element should be 15. Last
            element should be 6
        dt: the duration of each time step
    returns:
        scalar cost, given by the sum of the navigation function over time
    """
    # Run simulation
    turtle_states, box_states = mam_simulate_single_push_two_turtles(
        design_params,
        exogenous_sample,
        layer_widths,
        dt,
    )

    # Compute cost based on distance from final box pose to desired box pose
    desired_box_pose = exogenous_sample[4:7]
    final_box_pose = box_states[-1, :3]
    cost = ((desired_box_pose - final_box_pose) ** 2).sum()

    return cost
