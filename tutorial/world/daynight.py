# world/daynight.py

from evennia.contrib.base_systems import gametime
from evennia.utils import logger
import math

# -- CONFIGURATION -- #
SECONDS_PER_REAL_WORLD_HOUR = 3600  # 3600s = 1h real time
SECONDS_PER_GAME_DAY = SECONDS_PER_REAL_WORLD_HOUR  # 1 hour IRL = 1 in-game day

# Calendar settings
MONTHS = [
    ("January", 6),
    ("February", 7),
    ("March", 9),
    ("April", 11),
    ("May", 14),
    ("June", 16),
    ("July", 16),
    ("August", 14),
    ("September", 12),
    ("October", 10),
    ("November", 8),
    ("December", 6),
]

SEASONS = {
    "Winter": ["December", "January", "February"],
    "Spring": ["March", "April", "May"],
    "Summer": ["June", "July", "August"],
    "Autumn": ["September", "October", "November"],
}

# Phases of the day
DAWN_DURATION = 0.05  # 5% of day
TWILIGHT_DURATION = 0.05  # 5% of day


class GameTimeManager:
    def __init__(self):
        self.clock = gametime.gametime
        self.total_game_seconds = SECONDS_PER_GAME_DAY

    def get_time_info(self):
        """
        Calculate the current day, month, time etc.
        """
        seconds = self.clock.gametime(absolute=True) % self.total_game_seconds
        day_progress = seconds / self.total_game_seconds

        # Estimate the month/day
        month_index = (
            int((self.clock.gametime(absolute=True) / self.total_game_seconds) / 30)
            % 12
        )
        month_name, daylight_hours = MONTHS[month_index]
        season = self.get_season(month_name)

        return {
            "seconds": seconds,
            "day_progress": day_progress,
            "month": month_name,
            "daylight_hours": daylight_hours,
            "season": season,
        }

    def get_season(self, month_name):
        for season, months in SEASONS.items():
            if month_name in months:
                return season
        return "Unknown"

    def get_day_phase(self):
        """
        Return the current phase of the day: Night, Dawn, Day, Twilight
        """
        info = self.get_time_info()
        daylight_fraction = info["daylight_hours"] / 24

        # Calculate thresholds
        dawn_start = (0.5 - daylight_fraction / 2) - DAWN_DURATION
        day_start = dawn_start + DAWN_DURATION
        day_end = day_start + daylight_fraction
        twilight_start = day_end
        night_start = twilight_start + TWILIGHT_DURATION

        progress = info["day_progress"]

        if dawn_start <= progress < day_start:
            return "Dawn"
        elif day_start <= progress < twilight_start:
            return "Day"
        elif twilight_start <= progress < night_start:
            return "Twilight"
        else:
            return "Night"

    def announce_time_change(self):
        """
        Hook to broadcast or trigger events at phase changes.
        """
        phase = self.get_day_phase()
        season = self.get_time_info()["season"]
        month = self.get_time_info()["month"]

        logger.log_info(f"The current phase is {phase}. It is {month}, {season}.")
        # TODO: Expand this to actually notify players or spawn monsters, adjust weather, etc.


# Global instance
gametime_manager = GameTimeManager()
