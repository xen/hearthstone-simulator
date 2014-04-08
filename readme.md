Hearthstone Simulator
=====================

The purpose of this project is to create an open source Hearthstone simulator for the purposes of machine learning and
data mining of Blizzard's [Hearthstone: Heroes of WarCraft](http://battle.net/hearthstone).  The end goal
is to create a system implementing every card in Hearthstone, then simulate games of bots against bots to train
them.  The results from these games can be used to determine cards which work well together and cards which do not.
The goal is not to create a clone of Hearthstone which players can use to replace the game itself with.

Progress
--------

Currently, the main engine is mostly implemented, along with a few cards.  [cards.csv] is a listing of all cards in the
game along with information on which has been implemented.  Any card which has been implemented also has at least one
unit test to ensure that it works correctly

Structure
---------
Almost all of the game logic is found in [hsgame/game_objects.py].  The game functions largely on an event based system.
The events use a bind/trigger mechanism.  For example, a card which has a deathrattle will bind an event to its 'death'
event that takes the appropriate action.  Parameters can be passed to an event at the time it is bound, or the time it
is triggered, or both.  For an overview of the events and the parameters they receive, see [events.md].

The cards themselves are each a class, and can be found in the [hsgame/cards] directory, organized by type
(spell/minion/secret/weapon) and by class.

This project also includes a replay facility, which allows for games to be recorded and played back.  The format for
the replay syntax is documented in [replay_format.md].

_Hearthstone: Heroes of WarCraft_ and _Blizzard_ are trademarks of Blizzard Entertainment.