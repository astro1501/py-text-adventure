import json
import time
import random

def main():
    # TODO: allow them to choose from multiple JSON files?
    with open('adventure.json') as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)


def play(rooms):
    start_time = time.time()
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...', '3 quarters', '2 dimes']

    # allows us to see the whole dict: print(rooms)

    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])

        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.
        if current_place != "outside":
            temp = here['items']
            print("There is {} in this room".format(temp[0]))

        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Clears all locations of a cat then chooses random location to place a cat
        for all_rooms in rooms:
            if all_rooms != '__metadata__':
                rooms[all_rooms]['cat'] = False
        room_names = [] 
        for key in rooms.keys(): 
            room_names.append(key)   
        del room_names[0]
        rand_place = random.choice(room_names)
        rooms[rand_place]['cat'] = True
        if here.get("cat", True):
            print("A black cat has wandered into this room.")

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        if action == 'stuff':
            print(stuff)
            continue
        
        # Create a "push button" command, this is my big switch, it makes items appear
        if action == "push button":
            change_item = rooms["Cafeteria"]
            change_item['items'][0] = "Master key"
            print("You here something clatter on the floor, downstairs.")
            continue
        
        # If drop is typed, I am being lazy and only allowing one item to be
        # assigned to a room at once and you can only drop the last item picked up.
        if action == 'drop':
            here['items'][0] = stuff[len(stuff)-1]
            del stuff[len(stuff)-1]
            continue
        
        # TODO: if they type "take", grab any items in the room.
        if action == 'take':
            temp = here['items']
            if temp[0] != 'nothing':
                stuff.append(temp[0])
                here['items'][0] = "nothing"
                continue
            print("You can't take 'nothing', silly!")
            continue
            
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        if action == "search" or action == 'find':
            for exit in here['exits']:
                if exit.get("hidden", True):
                    exit["hidden"] = False
            continue    
        
        if action == 'help':
            print_instructions()
            continue
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            if "required_key" in selected:
                if selected["required_key"] in stuff:
                    current_place = selected['destination']
                else:
                    print("This room is locked. Search for the key.")
                    continue
            current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
    
    end_time = time.time()
    elapsed = end_time - start_time
    print("")
    print("")
    print("=== GAME OVER ===")
    print("Took you {} seconds to complete".format(int(elapsed)))

def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        usable.append(exit)
    return usable

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - 'push button' is a command that might come in handy.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()