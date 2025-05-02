"""
DayNightScript
This script manages the day/night cycle in the game.
It checks the time every minute and announces changes in the day/night cycle.
"""

from evennia import DefaultScript
from tutorial.world.time.daynight import gametime_manager


class DayNightScript(DefaultScript):
    def at_script_creation(self):
        self.key = "daynight_script"
        self.interval = 60  # Check every minute
        self.persistent = True

    def at_repeat(self):
        gametime_manager.announce_time_change()
