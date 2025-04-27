# in typeclasses/npcs.py

from evennia import DefaultCharacter


class OldMan(DefaultCharacter):
    """
    The frail elder, the last memory of a world lost to ruin.
    """

    def at_object_creation(self):
        self.db.desc = (
            "A gaunt old man with paper-thin skin and hollow eyes. His voice is barely a whisper, "
            "but every word is heavy with the weight of forgotten centuries."
        )
        self.db.health = 10  # Very frail
        self.db.charisma = 9  # Out of 10
        self.db.strength = 1
        self.db.influence = "low"
        self.locks.add("attack:false()")  # Maybe unattackable for now


class BossOscardian(DefaultCharacter):
    def at_object_creation(self):
        self.db.desc = (
            "Oscardian stands cloaked in filthy robes, chanting prayers to gods old and unknown. "
            "His eyes burn with feverish devotion."
        )
        self.db.religious = True
        self.db.charisma = 7  # Out of 10
        self.db.strength = 3
        self.db.influence = "low"


class BossMaximon(DefaultCharacter):
    def at_object_creation(self):
        self.db.desc = "Maximon rules with brutal authority. His steel gaze alone can quell dissent, and his fists do the rest."
        self.db.despot = True
        self.db.charisma = 5
        self.db.strength = 8
        self.db.influence = "high"


class Marlotte(DefaultCharacter):
    """
    Militant boss Marlotte, now a questgiver.
    """

    def at_object_creation(self):
        def at_object_creation(self):
            self.db.desc = (
                "Marlotte is a hardened fighter, scarred and unyielding. Her voice commands instant attention, "
                "and her presence promises discipline."
            )
            self.db.military = True
            self.db.charisma = 6
            self.db.strength = 7
            self.db.influence = "medium"
            self.db.quest_given = False

    def at_say(self, message, from_obj, **kwargs):
        """
        Listen for players talking to her.
        """
        if "job" in message.lower() or "work" in message.lower():
            if not self.db.quest_given:
                self.msg_contents(
                    "Marlotte says: 'Good, we got a rat problem down in the engine room. Kill at least 5 of them.'"
                )
                from_obj.db.quest = "rat_hunt"
                from_obj.db.rats_killed = 0
                self.db.quest_given = True
            else:
                self.msg_contents(
                    "Marlotte says: 'What are you waiting for? Get rid of those rats!'"
                )

    def at_look(self, looker):
        """
        Show the NPC's description when looked at.
        """
        looker.msg(f"{self.name} is here. {self.db.desc}")
        self.msg_contents(
            "Marlotte says: 'I don't have time for idle chatter. Get to work!'"
        )


# typeclasses/npcs.py


class Rat(DefaultCharacter):
    """
    A nasty, oversized rat chewing on supplies.
    """

    def at_object_creation(self):
        self.db.desc = (
            "An ugly, diseased-looking rat as big as a small dog. It looks vicious."
        )
        self.db.body_parts = {"body": 5}
        self.db.is_rat = True

    def die(self):
        """
        Notify killer if part of quest.
        """
        location = self.location
        killer = self.db.killer

        if killer and killer.db.quest == "rat_hunt":
            killer.db.rats_killed += 1
            killer.msg(f"|gYou have killed {killer.db.rats_killed}/5 rats!|n")
            if killer.db.rats_killed >= 5:
                killer.msg("|wReturn to Marlotte for your reward.|n")

        super().die()
        self.location.msg_contents(f"{self.name} dies with a squeak.")
