import sqlite3
import sys

conn = sqlite3.connect('pokemon.sqlite')
cursor = conn.cursor()

pokemon_ids = sys.argv[1:]

def analyze_pokemon(pokemon_id):
    cursor.execute("SELECT name, type1, type2, against_fire, against_water, against_grass, against_electric, against_ice, against_fighting, against_poison, against_ground, against_flying, against_psychic, against_bug, against_rock, against_ghost, against_dragon, against_dark, against_steel, against_fairy FROM pokemon WHERE id = ?", (pokemon_id,))
    result = cursor.fetchone()

    if result:
        name, type1, type2, *against = result[3:]

        # Determine the strengths and weaknesses of the Pokemon against different types
        strengths = []
        weaknesses = []

        types = ['fire', 'water', 'grass', 'electric', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']

        for type_, against_val in zip(types, against):
            if against_val > 1:
                strengths.append(type_)
            elif against_val < 1:
                weaknesses.append(type_)

        
        print(f"Analyzing {pokemon_id}")
        print(f"{name} ({type1} {type2}) is strong against {strengths} but weak against {weaknesses}")

        return True
    else:
        return False

team_analysis = []
for pokemon_id in pokemon_ids:
    if analyze_pokemon(pokemon_id):
        team_analysis.append(pokemon_id)


save_team = input("Would you like to save this team? (Y)es or (N)o: ").lower() == 'y'

if save_team:
    team_name = input("Enter the team name: ")
    cursor.execute("INSERT INTO teams (name, pokemon_ids) VALUES (?, ?)", (team_name, ' '.join(team_analysis)))
    conn.commit()
    print(f"Saving {team_name} ...")

conn.close()


# types
# for loop
# if else










