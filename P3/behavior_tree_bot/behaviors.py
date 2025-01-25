import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (2) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (3) Check if the strongest planet has enough ships to capture the weakest enemy planet.
        if strongest_planet.num_ships > weakest_planet.num_ships:
            # (4) Send half the ships from my strongest planet to the weakest enemy planet.
            return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
        else:
            # Not enough ships to capture the planet
            return False


def spread_to_weakest_neutral_planet(state):
    # (1) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (2) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (3) Check if the strongest planet has enough ships to capture the weakest enemy planet.
        if strongest_planet.num_ships > weakest_planet.num_ships:
            # (4) Send half the ships from my strongest planet to the weakest enemy planet.
            return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
        else:
            # Not enough ships to capture the planet
            return False

# Balance ships across planets by sending ships from overpopulated to underpopulated planets
def balance_fleets_action(state):
    # (1) If we currently have a 10 fleets in flight, just do nothing.
    if len(state.my_fleets()) >= 10:
        return False
    my_planets = state.my_planets()  # Get list of planets
    total_ships = sum(planet.num_ships for planet in my_planets)
    average_ships = total_ships / len(my_planets) if len(my_planets) > 0 else 0

    for planet in my_planets:  # Iterate over the list directly
        if planet.num_ships > average_ships:
            surplus_ships = planet.num_ships - average_ships
            # Find the planet with the least number of ships
            target_planet = min(my_planets, key=lambda p: p.num_ships, default=None)
            if target_planet:
                ships_to_send = min(surplus_ships, target_planet.num_ships)
                # Instead of modifying num_ships, issue the move order.
                if ships_to_send > 0:
                    issue_order(state, planet.ID, target_planet.ID, ships_to_send)
    return True
