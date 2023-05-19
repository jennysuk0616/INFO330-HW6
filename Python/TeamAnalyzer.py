import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
        "fire","flying","ghost","grass","ground","ice","normal",
        "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    
    pokemon_identifier = arg
    
    # Connect to the pokemon database
    conn = sqlite3.connect('../pokemon.sqlite')
    cursor = conn.cursor()
    
    # Retrieve the Pokemon information from the database
    cursor.execute("SELECT name, type1_name, type2_name, " + ", ".join(["against_" + type_ for type_ in types]) + " FROM pokemon_types_battle_view WHERE pokedex_number = ? OR name = ?", (pokemon_identifier, pokemon_identifier))
    result = cursor.fetchone()
    
    if result:
        name, type1, type2, *against = result[3:]
    
        # Determine the strengths and weaknesses of the Pokemon against different types
        strengths = [type_ for type_, against_val in zip(types, against) if against_val > 1]
        weaknesses = [type_ for type_, against_val in zip(types, against) if against_val < 1]
    
        # Print the analysis result
        print(f"Analyzing {pokemon_identifier}")
        print(f"{name} ({type1} {type2}) is strong against {strengths} but weak against {weaknesses}")

        team.append(str(result[0]))
    
    conn.close()

    # Analyze the pokemon whose pokedex_number is in "arg"

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")
    
    print("Saving " + teamName + " ...")
    
    conn.close()
else:
    print("Bye for now!")

