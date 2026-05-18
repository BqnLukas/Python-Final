SCREEN_WIDTH = 80
title = "Adventure Quest"

from character import character
from locations import game_map, items_at_location, location_description
from quests import quests
from save_load import save_game_state, load_game_state
from map import build_map_display, describe_location


def parse_coordinates(text: str) -> tuple[int, int] | None:
    text = text.replace(" ", "")
    if not text:
        return None
    parts = text.split(",")
    if len(parts) != 2:
        return None
    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError:
        return None
    if (x, y) in game_map:
        return x, y
    return None

#HEADER / main menu and character creation
if __name__ == "__main__":
    print("================================================================================")
    print("                                Adventure Quest")
    print("================================================================================")
    print("Welcome to Adventure Quest!")
    print()
    print("In this mystical land, you will embark on a thrilling journey to find the Enchanted Castle, rescue allies, and rebuild communities. Along the way, you will encounter various challenges, meet different characters, and collect valuable resources. Good luck on your adventure!")
    print()
    print("================================================================================")
    print("| Main Menu:                                                                    |")
    print("| 1. Start New Game                                                             |")
    print("| 2. Load Game                                                                  |")
    print("| 3. Quit                                                                       |")
    print("================================================================================")
    choice = input("Please select an option: ").strip()

    if choice == "1":
        print("================================================================================")
        print("                                Adventure Quest")
        print("================================================================================")
        print("Create your Character!")
        print()
        while True:
            raw = input("Enter your character's name: ").strip()
            if not raw:
                print("Name cannot be blank. Please enter a name.")
                continue
            if any(ch.isdigit() for ch in raw):
                print("Names cannot contain numbers. Please try again.")
                continue
            if not raw[0].isalpha():
                print("Name must start with a letter. Please try again.")
                continue
            name = raw[0].upper() + raw[1:]
            break
        player = character(name)

        print()
        print(f"Character created! Name: {player.name}, Health: {player.health}, Strength: {player.strength}")
        print()
        input("Press Enter to continue...")
        current_quests = {quest_name: quest_data.copy() for quest_name, quest_data in quests.items()}
        current_items = {coords: items.copy() for coords, items in items_at_location.items()}
        save_game_state(player, current_quests, current_items)
        run_game_loop(player, current_quests, current_items)
    elif choice == "2":
        save_data = load_game_state()
        if save_data is None:
            print("No saved game was found.")
        else:
            player_data = save_data["player_data"]
            player = character(player_data["name"])
            player.health = player_data["health"]
            player.strength = player_data["strength"]
            player.level = player_data["level"]
            player.gold = player_data["gold"]
            player.magic = save_data["player_data"]["magic"]
            player.inventory = save_data["inventory"]

            current_items = {coords: items.copy() for coords, items in save_data["items_at_location"].items()}
            current_quests = {quest_name: {"status": quest_data["status"]} for quest_name, quest_data in save_data["quests"].items()}

            print(f"Loaded {player.name}'s saved game.")
            run_game_loop(player, current_quests, current_items)

    elif choice == "3":
        print("Goodbye.")
    else:
        print("Invalid selection.")


def build_status_screen(player, location_name: str, coords: tuple[int, int]) -> str:
    border = "=" * SCREEN_WIDTH
    title = "Adventure Quest"
    loc_line = f"Location: {location_name} ({coords[0]}, {coords[1]})"

    def get_attr(p, key):
        if isinstance(p, dict):
            return p.get(key, "")
        return getattr(p, key, "")

    col1 = f"Name: {get_attr(player, 'name')}"
    col2 = f"Health: {get_attr(player, 'health')}"
    col3 = f"Strength: {get_attr(player, 'strength')}"
    line1 = f"| {col1:<20}{col2:<20}{col3:<30}|"

    col4 = f"Level: {get_attr(player, 'level')}"
    col5 = f"Gold: {get_attr(player, 'gold')}"
    col6 = f"Magic: {get_attr(player, 'magic')}"
    line2 = f"| {col4:<20}{col5:<20}{col6:<30}|"

    commands = [
        "| Available Commands:                                                           |",
        "| - Move: north (n), south (s), east (e), west (w)                              |",
        "| - Actions: inspect (c), interact (t)                                          |",
        "| - Item Actions - add [item_name]: pick up (p), drop (d), use (u)              |",
        "| - View Inventory (i)                                                          |",
        "| - View Map (m)                                                                |",
        "| - Quit (q)                                                                    |"
    ]

    return "\n".join([
        border,
        title.center(SCREEN_WIDTH),
        loc_line.center(SCREEN_WIDTH),
        border,
        line1,
        line2,
        border,
        *commands,
        border
    ])

def run_game_loop(player, current_quests, game_items):
    MIN_X, MAX_X = 0, 4
    MIN_Y, MAX_Y = 0, 4
    print()
    print("Game commands: n/s/e/w = move, m = map, i = inventory, p = pick up, d = drop, u = use, c = inspect, t = interact, s = save, q = quit")
    # ensure player has a location attribute
    if not hasattr(player, 'location'):
        player.location = (0, 0)

    while True:
        command = input("Enter command: ").strip().lower()

        # movement
        if command in ("n", "north", "s", "south", "e", "east", "w", "west"):
            x, y = player.location
            if command.startswith('n'):
                new = (x, y + 1)
            elif command.startswith('s'):
                new = (x, y - 1)
            elif command.startswith('e'):
                new = (x + 1, y)
            else:  # west
                new = (x - 1, y)
            nx, ny = new
            if nx < MIN_X or nx > MAX_X or ny < MIN_Y or ny > MAX_Y:
                print(f"You cannot move outside the map. Valid x,y range is {MIN_X}-{MAX_X}, {MIN_Y}-{MAX_Y}.")
                continue
            player.location = (nx, ny)
            loc_name = game_map.get(player.location, "Unknown")
            print(f"You move to {loc_name} {player.location}.")
            # auto-save after move
            save_game_state(player, current_quests, game_items)

        # map display and inspect by coords
        elif command == "m":
            print()
            print(build_map_display())
            coords_text = input("Enter coordinates as x,y to inspect a tile (or press Enter to return): ").strip()
            if not coords_text:
                continue
            coords = parse_coordinates(coords_text)
            if coords is None:
                print("Invalid coordinates. Use x,y where both are 0-4.")
                continue
            print(describe_location(coords))
            print()

        # inventory
        elif command == "i":
            inv = getattr(player, 'inventory', [])
            if not inv:
                print("Your inventory is empty.")
            else:
                print("Inventory:")
                for it in inv:
                    print(" - ", it)

        # pick up
        elif command == "p":
            loc = player.location
            items_here = game_items.get(loc, [])
            if not items_here:
                print("There is nothing to pick up here.")
                continue
            print("Items at this location:")
            for idx, it in enumerate(items_here, 1):
                print(f"{idx}. {it}")
            choice = input("Enter item number or name to pick up: ").strip()
            if not choice:
                continue
            # try number
            picked = None
            if choice.isdigit():
                i = int(choice) - 1
                if 0 <= i < len(items_here):
                    picked = items_here.pop(i)
            else:
                if choice in items_here:
                    items_here.remove(choice)
                    picked = choice
            if picked:
                player.inventory.append(picked)
                game_items[loc] = items_here
                print(f"Picked up {picked}.")
                save_game_state(player, current_quests, game_items)
            else:
                print("Could not pick that item.")

        # drop
        elif command == "d":
            inv = getattr(player, 'inventory', [])
            if not inv:
                print("You have no items to drop.")
                continue
            print("Your inventory:")
            for idx, it in enumerate(inv, 1):
                print(f"{idx}. {it}")
            choice = input("Enter item number or name to drop: ").strip()
            if not choice:
                continue
            dropped = None
            if choice.isdigit():
                i = int(choice) - 1
                if 0 <= i < len(inv):
                    dropped = inv.pop(i)
            else:
                if choice in inv:
                    inv.remove(choice)
                    dropped = choice
            if dropped:
                loc = player.location
                game_items.setdefault(loc, []).append(dropped)
                print(f"Dropped {dropped} at {loc}.")
                save_game_state(player, current_quests, game_items)
            else:
                print("Could not drop that item.")

        # use
        elif command == "u":
            inv = getattr(player, 'inventory', [])
            if not inv:
                print("You have no items to use.")
                continue
            print("Your inventory:")
            for idx, it in enumerate(inv, 1):
                print(f"{idx}. {it}")
            choice = input("Enter item number or name to use: ").strip()
            if not choice:
                continue
            used = None
            if choice.isdigit():
                i = int(choice) - 1
                if 0 <= i < len(inv):
                    used = inv.pop(i)
            else:
                if choice in inv:
                    inv.remove(choice)
                    used = choice
            if used:
                print(f"You use the {used}. Nothing dramatic happens.")
                save_game_state(player, current_quests, game_items)
            else:
                print("Could not use that item.")

        # inspect current tile
        elif command == "c":
            print(describe_location(player.location))

        # interact
        elif command == "t":
            print("There is nothing in particular to interact with here.")

        # save
        elif command == "s":
            save_game_state(player, current_quests, game_items)
            print("Game saved.")

        # quit
        elif command == "q":
            save_game_state(player, current_quests, game_items)
            print("Game saved and exiting. Goodbye.")
            break

        else:
            print("Unknown command. Valid commands: n/s/e/w, m, i, p, d, u, c, t, s, q")


