"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom

from evennia import DefaultRoom

from .objects import ObjectParent


class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Objects.
    """

    pass


class ArkStartRoom(DefaultRoom):
    """
    The initial starting room aboard the rusted-out Ark (the cruise ship).
    """

    def at_object_creation(self):
        self.db.desc = (
            "The dim corridors of the Ark reek of rust, mildew, and human desperation. "
            "Dim emergency lights flicker along walls warped by time and decay. "
            "The ship lists dangerously to starboard, groaning with each gust of coastal wind. "
            "You see improvised bunk beds, tarps stretched into shelters, and frightened, hungry eyes watching you."
        )
        self.locks.add("get:false()")  # Players can't 'get' the room accidentally.
