from locations import game_map, location_description

CELL_WIDTH = 20
GRID_SIZE = 5


def _format_cell(text: str, width: int = CELL_WIDTH) -> str:
    trimmed = text[:width]
    return f" {trimmed.center(width - 2)} "


def build_map_display() -> str:
    horizontal = "+" + "+".join(["-" * CELL_WIDTH for _ in range(GRID_SIZE)]) + "+"
    lines = ["MAP", horizontal]
    for y in range(GRID_SIZE):
        row_cells = []
        for x in range(GRID_SIZE):
            location_name = game_map.get((x, y), "Unknown")
            row_cells.append(_format_cell(location_name))
        lines.append("|" + "|".join(row_cells) + "|")
        lines.append(horizontal)
    return "\n".join(lines)


def describe_location(coords: tuple[int, int]) -> str:
    if coords not in game_map:
        return "There is no location at those coordinates."
    location_name = game_map[coords]
    description = location_description.get(location_name, "No description is available for this location.")
    return f"{location_name} ({coords[0]},{coords[1]}): {description}"
