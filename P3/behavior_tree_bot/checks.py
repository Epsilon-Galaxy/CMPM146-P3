def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def balance_fleets(state):
    if len(state.my_planets()) <= len(state.enemy_planets()):
        return False

    total_ships = sum(planet.num_ships for planet in state.my_planets())
    average_ships = total_ships / len(state.my_planets()) if len(state.my_planets()) > 0 else 0
    imbalance_threshold = 0.1  # Threshold to trigger balancing

    # Find planets with significantly more ships than average
    for planet in state.my_planets():
        if planet.num_ships > average_ships * (1 + imbalance_threshold):
            # Check if we need to send ships to planets with fewer ships
            return True

    return False