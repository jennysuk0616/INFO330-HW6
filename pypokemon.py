import sqlite3 # This is the package for all sqlite3 access in Python
import sys # This helps with command-line parameters

# Connect to the pokemon database
conn = sqlite3.connect('pokemon.sqlite')
c = conn.cursor()

# Take in the Pokedex numbers from command-line arguments
pokedex_numbers = sys.argv[1:]

# Analyze each Pokemon against all types
for number in pokedex_numbers:
    c.execute("SELECT name, type1, type2, against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water FROM pokemon WHERE number=?", (number,))
    pokemon_data = c.fetchone()
    name = pokemon_data[0]
    type1 = pokemon_data[1]
    type2 = pokemon_data[2]
    against = []
    weak = []
    for i in range(3, 22):
        if pokemon_data[i] > 1:
            against.append(c.description[i][0][8:])
        elif pokemon_data[i] < 1:
            weak.append(c.description[i][0][8:])
    print(f"Analyzing {number}")
    print(f"{name} ({type1} {type2 if type2 else ''}) is strong against {against} but weak against {weak}")

# Ask if the team is worth saving
save = input("Would you like to save this team? (Y)es or (N)o: ")
if save.lower() == 'y':
    # Insert team data into teams table
    team_name = input("Enter the team name: ")
    c.execute("INSERT INTO teams (name, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (team_name, *pokedex_numbers))
    print(f"Saving Team {team_name} ...")

# Commit changes and close the connection
conn.commit()
conn.close()



