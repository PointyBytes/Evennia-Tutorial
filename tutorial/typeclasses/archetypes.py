class Archetype:
    """
    Base class for all character archetypes.
    Defines structure for skills and perk unlocks.
    """

    def __init__(self, character):
        self.character = character
        self.starting_skills = []
        self.perks = {}

    def at_assign(self):
        """
        Called when the archetype is assigned to a character.
        Override in subclasses to set up special skills, etc.
        """
        pass

    def get_available_perks(self, level):
        """
        Return a list of perks unlocked at the given level.
        """
        return [perk for lvl, perk in self.perks.items() if lvl <= level]


class Boss(Archetype):
    def __init__(self, character):
        super().__init__(character)
        self.starting_skills = ["Command"]
        self.perks = {
            1: "Speechcraft",
            5: "Mobilize Troops",
            10: "Unshakable Authority",
        }

    def at_assign(self):
        self.character.db.skills = self.starting_skills
        self.character.db.archetype = "Boss"


class Stalker(Archetype):
    def __init__(self, character):
        super().__init__(character)
        self.starting_skills = ["Find the Way"]
        self.perks = {
            1: "Forager",
            5: "Ambusher",
            10: "Pathfinder",
        }

    def at_assign(self):
        self.character.db.skills = self.starting_skills
        self.character.db.archetype = "Stalker"


class BlackThumb(Archetype):
    def __init__(self, character):
        super().__init__(character)
        self.starting_skills = ["Crafting"]
        self.perks = {
            1: "Quick Fix",
            5: "Master Crafter",
            10: "Artisan's Touch",
        }

    def at_assign(self):
        self.character.db.skills = self.starting_skills
        self.character.db.archetype = "Black Thumb"


class Historian(Archetype):
    def __init__(self, character):
        super().__init__(character)
        self.starting_skills = ["Lorekeeper"]
        self.perks = {
            1: "Ancient Knowledge",
            5: "Linguist",
            10: "Archivist's Mind",
        }

    def at_assign(self):
        self.character.db.skills = self.starting_skills
        self.character.db.archetype = "Historian"


class BodyMechanic(Archetype):
    def __init__(self, character):
        super().__init__(character)
        self.starting_skills = ["Healing"]
        self.perks = {
            1: "Field Medic",
            5: "Herbalist",
            10: "Surgeon",
        }

    def at_assign(self):
        self.character.db.skills = self.starting_skills
        self.character.db.archetype = "Body Mechanic"


class Scavenger(Archetype):
    def __init__(self, character):
        super().__init__(character)
        self.starting_skills = ["Scavenging"]
        self.perks = {
            1: "Treasure Hunter",
            5: "Resourceful",
            10: "Master Scavenger",
        }

    def at_assign(self):
        self.character.db.skills = self.starting_skills
        self.character.db.archetype = "Scavenger"


class Fighter(Archetype):
    def __init__(self, character):
        super().__init__(character)
        self.starting_skills = ["Combat"]
        self.perks = {
            1: "Brawler",
            5: "Tactician",
            10: "Warrior's Spirit",
        }

    def at_assign(self):
        self.character.db.skills = self.starting_skills
        self.character.db.archetype = "Fighter"
