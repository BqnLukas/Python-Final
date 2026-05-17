class item:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value


# Consumables
consumables = {
    "potions": {
        "Health Potion": {"health": 20, "value": 10},
        "Super Health Potion": {"health": 50, "value": 25},
        "Mana Potion": {"magic": 20, "value": 10},
        "Stamina Elixir": {"stamina": 20, "value": 15}
    },
    "scrolls": {
        "Magic Scroll": {"magic": 10, "value": 25},
        "Ancient Scroll": {"level": 1, "value": 100},
    },
    "food": {
        "Sweetroll": {"message": "You ate the sweetroll.", "health": 5, "value": 4},
        "Wheel of Cheese": {"message": "You ate the wheel of cheese... Wow, that was a lot.", "health": 10, "value": 8},
        "Fungal Fritter": {"message": "You ate the fungal fritter. Surprisingly tasty!", "health": 8, "value": 5},
        "Honeyed Apple": {"message": "You ate the honeyed apple.", "health": 6, "value": 3},
        "Spiced Jerky": {"message": "You chewed the spiced jerky.", "health": 8, "value": 6},
        "Berry Tart": {"message": "You ate the berry tart.", "health": 7, "value": 5},
        "Mushroom Stew": {"message": "You ate the mushroom stew.", "health": 12, "value": 10}
    },
    "drinks": {
        "Carton of Milk": {"message": "You drank the milk.", "health": 5, "value": 2},
        "Dr. Pepper": {"message": "You drank the Dr. Pepper.", "health": 5, "value": 3},
        "Water": {"message": "You drank the water.", "health": 2, "value": 2},
        "Herbal Tea": {"message": "You drank the herbal tea.", "health": 4, "value": 3},
        "Fizzy Soda": {"message": "You drank the fizzy soda.", "health": 3, "value": 3},
        "Pure Spring Water": {"message": "You drank the pure spring water.", "health": 5, "value": 4},
        "Spiced Cider": {"message": "You drank the spiced cider.", "health": 6, "value": 5}
    },
    "misc": {
        "Daily Newspaper": {"message": "It wasn't much good... Mostly just advertisements and political campaign gossip.", "value": 2},
        "Old Map": {"message": "A worn map showing forgotten roads.", "value": 8},
    }
}


# Equippables
equippables = {
    "armor_and_jewelery": {
        "Chestplate": {"maxhealth": 20, "maxequipped": 1, "value": 15},
        "Leggings": {"maxhealth": 15, "maxequipped": 1, "value": 12},
        "Boots": {"maxhealth": 5, "maxequipped": 1, "value": 5},
        "Helmet": {"maxhealth": 10, "maxequipped": 1, "value": 7},
        "Gloves": {"maxhealth": 5, "maxequipped": 1, "value": 5},
        "Enchanted Amulet": {"message": "An amulet radiating strange magic.", "maxhealth": 20, "maxequipped": 1, "value": 80},
    },
    "weapons_and_shields": {
        "Shield": {"message": "Shield has no effect outside of combat.", "strength": 10, "maxequipped": 1, "value": 8},
        "Rusty Sword": {"message": "Rusty sword has no effect outside of combat.", "strength": 10, "maxequipped": 1, "value": 10},
        "Simple Wooden Sword": {"message": "Simple wooden sword has no effect outside of combat.", "strength": 15, "maxequipped": 1, "value": 15},
        "Iron Longsword": {"message": "Iron longsword has no effect outside of combat.", "strength": 25, "maxequipped": 1, "value": 50}
    }
}


# Currency
currency_values = {
    "gold": 1.0,
    "silver": 0.1,
    "copper": 0.01
}

currency = {
    "Gold Coin": {"gold": 1, "value": 1},
    "Silver Coin": {"gold": 0.1, "value": 0.1},
    "Copper Coin": {"gold": 0.01, "value": 0.01}
}


# Monster Loot
monster_loot = {
    "Feral Beast Fang": {"message": "A sharp fang from a feral beast.", "value": 12},
    "Spider's Venom": {"message": "A vial of potent spider venom.", "value": 15},
    "Shadow's Soul": {"message": "A trapped soul from the shadows.", "value": 20},
    "Toad's Eye Amulet": {"message": "A strange amulet with mysterious power... Maybe it could be sold.", "value": 150},
    "Bone McGee's Golden Dentures": {"message": "A ridiculous but valuable set of golden dentures.", "value": 95},
    "Dragon's Hoard": {"message": "A small chunk of treasure lifted from a dragon's hoard.", "gold": 50, "value": 50}
}



item_effects = {}
for category in (consumables, equippables):
    for subsection in category.values():
        item_effects.update(subsection)
item_effects.update(currency)
item_effects.update(monster_loot)

item_categories = {
    "Consumables": consumables,
    "Equippables": equippables,
    "Currency": currency,
    "Monster Loot": monster_loot
}