import json

# This global dictionary stores the name of the room as the key and the dictionary describing the room as the value.
GAME = {
    '__metadata__': {
        'title': 'Adventure',
        'start': 'classroom'
    }
}

def create_room(name, description, items, ends_game=False, cat=False):
    """
    Create a dictionary that represents a room in our game.

    INPUTS:
     name: string used to identify the room; think of this as a variable name.
     description: string used to describe the room to the user.
     ends_game: boolean, True if arriving in this room ends the game.
    
    RETURNS:
     the dictionary describing the room; also adds it to GAME!
    """
    assert (name not in GAME)
    room = {
        'name': name,
        'description': description,
        'exits': [],
        'items': [],
        'cat': cat
    }
    
    room['items'].append(items)
    
    # Does this end the game?
    if ends_game:
        room['ends_game'] = ends_game

    # Stick it into our big dictionary of all the rooms.
    GAME[name] = room
    return room

def create_exit(source, destination, description, required_key=None, hidden=False):
    """
    Rooms are useless if you can't get to them! This function connects source to destination (in one direction only.)

    INPUTS:
     source: which room to put this exit into (or its name)
     destination: where this exit goes (or its name)
     description: how to show this exit to the user (ex: "There is a red door.")
     required_key (optional): string of an item that is needed to open/reveal this door.
     hidden (optional): set this to True if you want this exit to be hidden initially; until the user types 'search' in the source room.
    """
    # Make sure source is our room!
    if isinstance(source, str):
        source = GAME[source]
    # Make sure destination is a room-name!
    if isinstance(destination, dict):
        destination = destination['name']
    # Create the "exit":
    exit = {
        'destination': destination,
        'description': description,
        'hidden' : hidden
    }
    if required_key:
        exit['required_key'] = required_key
    
    source['exits'].append(exit)
    return exit

##
# Let's imagine 4 places:
# Note that earlier, in __metadata__ we said that we should start in classroom.
##
classroom = create_room("classroom", "You're in a lecture hall, for some reason.", "Principle's ID")

hallway = create_room("hallway", "This is a hallway with many locked doors.", "nothing")

principle_office = create_room("Principles Office", "The drawers and shelves are overflowing with loose papers and confiscated objectes", "nothing")

under_desk = create_room("Under Principle's desk", "A small red button is tucked in the back corner.", "nothing")

janitors_closet = create_room("Janitor closet", "There are many wierd items scattered around.", "nothing")

crawl_space = create_room("Crawl Space", "Hidden room behind utility shelf", "Janitor's key")

staircase = create_room("staircase", "The staircase leads downward.", "nothing")

cafeteria = create_room("Cafeteria", "Moldy food is strewn across the ground", "nothing")

outside = create_room("outside", "You've escaped! It's cold out.", "nothing", ends_game=True)

##
# Let's connect them together.
# It's not a very fun adventure, but it's simple.
##
create_exit(classroom, hallway, "A door leads into the hall.")

# If you want doors to work in both directions; you have to do that yourself.
create_exit(hallway, classroom, "Go back into the classroom.")
create_exit('hallway', 'staircase', "A door with the words STAIRS is stuck open.")
create_exit(hallway, janitors_closet, "A door with a crooked janitors sign is locked")
create_exit(hallway, principle_office, "Door seems bolted shut", required_key="Principle's ID")

create_exit(principle_office, under_desk, "If always wondered what the bottom of a desk looked like.")
create_exit(principle_office, hallway, "This reminds me of trips to the office, lets leave.")

create_exit(under_desk, principle_office, "Let's get out from under here, it smells like old sandwiches and dirty socks!")

create_exit(janitors_closet, hallway, "Nothing in here, turn around")
create_exit(janitors_closet, crawl_space, "There are scratch marks on the wall.", hidden=True)

create_exit(crawl_space, janitors_closet, "Nothing else in here.")

create_exit(cafeteria, staircase, "Is that a dead rat!! I gotta go!")

create_exit(staircase, hallway, "Nevermind; go back to the hallway.")
create_exit(staircase, cafeteria, "I smell something funky through here", required_key="Janitor's key")
create_exit(staircase, outside, "A door at the bottom of the stairs has a red, glowing, EXIT sign.", required_key="Master key")
# we don't go back from outside, because the game ends as soon as we get there.

##
# Save our text-adventure to a file:
##
with open('adventure.json', 'w') as out:
    json.dump(GAME, out, indent=2)
