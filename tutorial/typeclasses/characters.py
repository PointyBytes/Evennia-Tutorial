"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent
import random


class Character(ObjectParent, DefaultCharacter):
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.


    Extended Character with tactical combat system.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.body_parts = {
            "head": 10,
            "torso": 20,
            "left_arm": 10,
            "right_arm": 10,
            "left_leg": 10,
            "right_leg": 10,
        }
        self.db.status_effects = []
        self.db.is_dead = False

    def take_damage(self, amount, part=None, severe_chance=0.2):
        """
        Apply damage to a body part.
        Randomly severe injuries.
        TODO: add bleeding, infection, etc.
        """
        if not part:
            part = random.choice(list(self.db.body_parts.keys()))

        self.msg(f"You are hit in the {part} for {amount} damage!")

        self.db.body_parts[part] -= amount

        if self.db.body_parts[part] <= 0:
            self.msg(f"Severe injury! Your {part} is disabled!")
            self.db.status_effects.append(f"{part}_disabled")

            if part == "head" or part == "torso":
                self.msg("|rFatal wound!|n")
                self.die()

        elif random.random() < severe_chance:
            self.msg(f"|ySevere damage to your {part}!|n")
            self.db.status_effects.append(f"{part}_injured")

        self.check_overall_health()

    def check_overall_health(self):
        """
        Check if character is still alive.
        """
        total_health = sum(self.db.body_parts.values())
        if total_health <= 0:
            self.msg("|rYou have succumbed to your wounds.|n")
            self.die()

    def die(self):
        """
        Handle death.
        This is a placeholder for now.

        TODO: respawning, loot drops, etc.
        """
        self.db.is_dead = True
        self.location.msg_contents(f"{self.key} collapses and dies!")
        self.delete()  # Simple for now, will expand later
