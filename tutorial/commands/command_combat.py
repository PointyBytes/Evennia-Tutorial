from evennia import Command
import random


class CmdAttack(Command):
    """
    Attack another creature or person.

    Usage:
      attack <target>
    """

    key = "attack"
    locks = "cmd:all()"

    def func(self):
        if not self.args:
            self.caller.msg("Attack whom?")
            return

        target = self.caller.search(self.args)
        if not target:
            return

        if not hasattr(target, "take_damage"):
            self.caller.msg("You can't attack that.")
            return

        damage = random.randint(1, 5)
        part = random.choice(list(target.db.body_parts.keys()))
        target.take_damage(damage, part=part)

        if hasattr(target, "db"):
            target.db.killer = self.caller
