"""
Prompts the user for a weight on Earth
and prints the equivalent weight on a selected planet.
"""

def main():
    # Dictionary of gravity factors relative to Earth
    gravity_factors = {
        "mercury": 0.38,
        "venus": 0.91,
        "earth": 1.00,
        "moon": 0.166,
        "mars": 0.378,
        "jupiter": 2.36,
        "saturn": 0.92,
        "uranus": 0.89,
        "neptune": 1.13,
        "pluto": 0.06
    }

    try:
        # Prompt user for Earth weight
        earth_weight = float(input("Enter a weight on Earth : "))

        # Prompt user for planet name
        planet = input("Enter the name of a planet: ").lower()

        # Check if planet is in the dictionary
        if planet in gravity_factors:
            gravity = gravity_factors[planet]
            planet_weight = round(earth_weight * gravity, 2)
            print(f"The equivalent weight on {planet.capitalize()}: {planet_weight} ")
        else:
            print("Invalid planet name. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a number for the weight.")

if __name__ == "__main__":
    main()
