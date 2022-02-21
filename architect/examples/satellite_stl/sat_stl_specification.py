import jax.numpy as jnp

import architect.components.specifications.stl as stl


def make_sat_rendezvous_specification() -> stl.STLFormula:
    """Makes the STL specification for the satellite rendezvous problem.

    This specification captures the following requirements:
        - If the chaser speed is too high, do not approach the target
        - Eventually enter a ring around the target and stay there for a bit
        - After staying in that ring for a while, approach the target
    """
    ################################################
    #   Make predicates
    ################################################

    # Make a predicate for the speed being below some threshold
    # Jewison and Erwin put this as 5 cm/s, so consider decreasing this value to match
    speed_threshold = 0.1  # m/s
    mu_negative_speed = lambda q_t: -jnp.linalg.norm(q_t[3:])  # 1-lipschitz
    p_low_speed = stl.STLPredicate(mu_negative_speed, -speed_threshold)

    # Make a predicate for being docked with the chaser satellite
    docking_threshold = 0.1  # m
    mu_negative_distance = lambda q_t: -jnp.linalg.norm(q_t[:3])  # 1-lipschitz
    p_docked = stl.STLPredicate(mu_negative_distance, -docking_threshold)

    # Make a predicate for being outside the min waiting radius
    min_waiting_radius = 2.0  # m
    mu_distance = lambda q_t: jnp.linalg.norm(q_t[:3])  # 1-lipschitz
    p_outside_min_radius = stl.STLPredicate(mu_distance, min_waiting_radius)

    # Make a predicate for being inside the max waiting radius
    max_waiting_radius = 3.0  # m
    p_inside_max_radius = stl.STLPredicate(mu_negative_distance, -max_waiting_radius)

    ################################################
    #   Define times for the mission
    ################################################
    min_time_in_waiting_zone = 10.0

    ################################################
    #   Construct the STL formula for the mission
    ################################################

    # Maintain separation from the target until speed is low enough, and maintain low
    # low speed during approch
    safety_constraint = stl.STLUntimedUntil(
        p_outside_min_radius, stl.STLUntimedAlways(p_low_speed)
    )

    # Reach the target before the end of the trajectory
    eventually_reach_target = stl.STLUntimedEventually(p_docked)

    # Reach the waiting zone before the given time and stay there for the specified
    # interval
    stay_inside_waiting_zone = stl.STLTimedAlways(
        stl.STLAnd(p_inside_max_radius, p_outside_min_radius),
        0.0,
        min_time_in_waiting_zone,
    )
    eventually_reach_waiting_zone_and_wait = stl.STLUntimedEventually(
        stay_inside_waiting_zone,
    )

    # Combine to mission requirement
    mission_spec = stl.STLAnd(
        safety_constraint,
        stl.STLAnd(eventually_reach_waiting_zone_and_wait, eventually_reach_target),
    )

    return stl.STLAnd(safety_constraint, eventually_reach_target)