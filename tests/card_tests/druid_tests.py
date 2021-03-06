from unittest.mock import Mock, call
from hsgame.constants import CHARACTER_CLASS

from hsgame.game_objects import Game
from hsgame.replay import SavedGame
from tests.testing_agents import *


__author__ = 'Daniel'

import random
from tests.testing_utils import generate_game_for, StackedDeck
from hsgame.cards import *
import unittest


class TestDruid(unittest.TestCase):

    def setUp(self):
        random.seed(1857)

    def test_Innervate(self):
        game = generate_game_for(Innervate, StonetuskBoar, SelfSpellTestingAgent, DoNothingBot)
        #triggers all four innervate cards the player is holding.
        game.play_single_turn()
        self.assertEqual(9, game.current_player.mana)

    def test_Moonfire(self):
        game = generate_game_for(Moonfire, StonetuskBoar, EnemySpellTestingAgent, MinionPlayingAgent)
        game.play_single_turn()
        self.assertEqual(26, game.other_player.health)

    def test_Claw(self):
        testing_env = self

        class ClawAgent(EnemySpellTestingAgent):
            def do_turn(self, player):
                super().do_turn(player)
                testing_env.assertEqual(2, self.game.current_player.attack_power)
                testing_env.assertEqual(2, self.game.current_player.armour)

        game = generate_game_for(Claw, StonetuskBoar, ClawAgent, MinionPlayingAgent)
        game.pre_game()
        game.play_single_turn()

    def test_Naturalize(self):
        game = generate_game_for(StonetuskBoar, Naturalize, MinionPlayingAgent, EnemyMinionSpellTestingAgent)
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(0, len(game.other_player.minions))
        self.assertEqual(5, len(game.other_player.hand))

    def test_Savagery(self):
        class SavageryAgent(EnemyMinionSpellTestingAgent):
            def do_turn(self, player):
                if player.mana > 2:
                    player.power.use()
                    super().do_turn(player)

        game = generate_game_for(Savagery, BloodfenRaptor, SavageryAgent, MinionPlayingAgent)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(1, len(game.other_player.minions))
        self.assertEqual(1, game.other_player.minions[0].defense)

    def test_ClawAndSavagery(self):
        deck1 = StackedDeck([BloodfenRaptor()], CHARACTER_CLASS.PRIEST)
        deck2 = StackedDeck([Claw(), Claw(), Savagery()], CHARACTER_CLASS.DRUID)
        game = Game([deck1, deck2], [MinionPlayingAgent(), EnemyMinionSpellTestingAgent()])
        game.current_player = game.players[1]
        game.pre_game()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(1, len(game.current_player.minions))

        game.play_single_turn()

        self.assertEqual(0, len(game.other_player.minions))

    def test_MarkOfTheWild(self):
        game = generate_game_for(MarkOfTheWild, StonetuskBoar, EnemyMinionSpellTestingAgent, MinionPlayingAgent)
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        self.assertEqual(3, game.other_player.minions[0].attack_power)
        self.assertEqual(3, game.other_player.minions[0].defense)
        self.assertEqual(3, game.other_player.minions[0].max_defense)

        #Test that this spell is being silenced properly as well
        game.other_player.minions[0].silence()
        self.assertEqual(1, game.other_player.minions[0].attack_power)
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(1, game.other_player.minions[0].max_defense)

    def test_PowerOfTheWild(self):
        deck1 = StackedDeck([StonetuskBoar(), StonetuskBoar(), PowerOfTheWild()], CHARACTER_CLASS.DRUID)
        deck2 = StackedDeck([StonetuskBoar()], CHARACTER_CLASS.MAGE)

        #This is a test of the +1/+1 option of the Power Of the Wild Card
        game = Game([deck1, deck2], [MinionPlayingAgent(), MinionPlayingAgent()])
        game.current_player = game.players[1]

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        self.assertEqual(2, game.current_player.minions[0].attack_power)
        self.assertEqual(2, game.current_player.minions[0].defense)
        self.assertEqual(2, game.current_player.minions[0].max_defense)
        self.assertEqual(2, game.current_player.minions[1].attack_power)
        self.assertEqual(2, game.current_player.minions[1].max_defense)

        #This is a test of the "Summon Panther" option of the Power of the Wild Card

        agent = MinionPlayingAgent()
        agent.choose_option = Mock(side_effect=lambda *options: options[1])

        deck1 = StackedDeck([StonetuskBoar(), StonetuskBoar(), PowerOfTheWild()], CHARACTER_CLASS.DRUID)
        deck2 = StackedDeck([StonetuskBoar()], CHARACTER_CLASS.MAGE)
        game = Game([deck1, deck2], [agent, MinionPlayingAgent()])
        game.current_player = game.players[1]

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual("Panther", game.current_player.minions[2].card.__class__.__name__)
        self.assertEqual(3, game.current_player.minions[2].attack_power)
        self.assertEqual(2, game.current_player.minions[2].max_defense)

    def test_WildGrowth(self):
        game = generate_game_for(WildGrowth, StonetuskBoar, SelfSpellTestingAgent, DoNothingBot)
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        self.assertEqual(3, game.current_player.max_mana)

    def test_Wrath(self):
        game = generate_game_for(Wrath, StonetuskBoar, EnemyMinionSpellTestingAgent, MinionPlayingAgent)
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(1, len(game.current_player.minions))

        game.play_single_turn()

        self.assertEqual(0, len(game.other_player.minions))
        self.assertEqual(5, len(game.current_player.hand))

        random.seed(1857)
        game = generate_game_for(Wrath, MogushanWarden, EnemyMinionSpellTestingAgent, MinionPlayingAgent)
        game.players[0].agent.choose_option = Mock(side_effect=lambda one, three: three)
        for turn in range(0, 8):
            game.play_single_turn()

        self.assertEqual(1, len(game.current_player.minions))

        game.play_single_turn()

        self.assertEqual(1, len(game.other_player.minions))
        #Two wraths will have been played
        self.assertEqual(1, game.other_player.minions[0].defense)

    def test_HealingTouch(self):
        game = generate_game_for(HealingTouch, StonetuskBoar, SelfSpellTestingAgent, DoNothingBot)
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.other_player.health = 20
        game.play_single_turn()
        self.assertEqual(28, game.current_player.health)
        game.play_single_turn()
        game.play_single_turn()
        self.assertEqual(30, game.current_player.health)

    def test_MarkOfNature(self):
        deck1 = StackedDeck([StonetuskBoar(), StonetuskBoar(), MarkOfNature()], CHARACTER_CLASS.DRUID)
        deck2 = StackedDeck([StonetuskBoar()], CHARACTER_CLASS.MAGE)
        game = Game([deck1, deck2], [MinionPlayingAgent(), MinionPlayingAgent()])

        game.current_player = 1
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(5, game.other_player.minions[0].attack_power)

        def mock_choose(*options):
            return options[1]
        deck1 = StackedDeck([StonetuskBoar(), StonetuskBoar(), MarkOfNature()], CHARACTER_CLASS.DRUID)
        deck2 = StackedDeck([StonetuskBoar()], CHARACTER_CLASS.MAGE)
        agent = MinionPlayingAgent()
        agent.choose_option = Mock(side_effect=mock_choose)
        game = Game([deck1, deck2], [agent, MinionPlayingAgent()])

        game.current_player = 1
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(5, game.other_player.minions[0].max_defense)
        self.assertEqual(5, game.other_player.minions[0].defense)
        self.assertTrue(game.other_player.minions[0].taunt)

    def test_SavageRoar(self):
        deck1 = StackedDeck([StonetuskBoar(), StonetuskBoar(), SavageRoar()], CHARACTER_CLASS.DRUID)
        deck2 = StackedDeck([StonetuskBoar()], CHARACTER_CLASS.MAGE)
        game = Game([deck1, deck2], [MinionPlayingAgent(), MinionPlayingAgent()])

        game.current_player = 1
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        minion_increase_mock = Mock()

        game.other_player.minions[0].bind("attack_increased", minion_increase_mock)
        game.other_player.minions[1].bind("attack_increased", minion_increase_mock)

        player_increase_mock = Mock()

        game.other_player.bind("attack_increased", player_increase_mock)


        game.play_single_turn()

        self.assertEqual(0, game.current_player.mana)

        #Make sure the attack got increased
        self.assertListEqual([call(2), call(2)], minion_increase_mock.call_args_list)
        self.assertListEqual([call(2)], player_increase_mock.call_args_list)

        #And make sure that it went down again
        self.assertEqual(0, game.current_player.minions[0].temp_attack)
        self.assertEqual(0, game.current_player.minions[1].temp_attack)
        self.assertEqual(0, game.current_player.attack_power)

    def test_Bite(self):
        testing_env = self

        class BiteAgent(EnemySpellTestingAgent):
            def do_turn(self, player):
                super().do_turn(player)
                if player.mana == 0:
                    testing_env.assertEqual(4, self.game.current_player.attack_power)
                    testing_env.assertEqual(4, self.game.current_player.armour)

        game = generate_game_for(Bite, StonetuskBoar, BiteAgent, DoNothingBot)
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

    def test_SoulOfTheForest(self):
        game = SavedGame("tests/replays/card_tests/SoulOfTheForest.rep")
        game.start()
        self.assertEqual(2, len(game.other_player.minions))
        self.assertEqual(2, game.other_player.minions[1].attack_power)
        self.assertEqual(2, game.other_player.minions[1].defense)
        self.assertEqual("Treant", game.other_player.minions[1].card.name)

    def test_Swipe(self):
        deck1 = StackedDeck([BloodfenRaptor(), StonetuskBoar(), StonetuskBoar()],CHARACTER_CLASS.DRUID)
        deck2 = StackedDeck([Swipe()], CHARACTER_CLASS.DRUID,)
        game = Game([deck1, deck2], [MinionPlayingAgent(), EnemyMinionSpellTestingAgent()])
        game.pre_game()
        game.current_player = game.players[1]
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        spell_damage_mock = Mock()
        game.current_player.minions[0].bind('spell_damaged', spell_damage_mock)
        game.current_player.minions[1].bind('spell_damaged', spell_damage_mock)
        game.current_player.minions[2].bind('spell_damaged', spell_damage_mock)
        swipe_card = game.other_player.hand[0]
        game.play_single_turn()

        self.assertListEqual([call(4, swipe_card), call(1, swipe_card), call(1, swipe_card)],
                             spell_damage_mock.call_args_list)

        #The bloodfen raptor should be left, with one hp
        self.assertEqual(1, len(game.other_player.minions))
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(29, game.other_player.health)


    def test_KeeperOfTheGrove(self):
        #Test Moonfire option

        game = generate_game_for(KeeperOfTheGrove, StonetuskBoar, MinionPlayingAgent, MinionPlayingAgent)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(3, len(game.current_player.minions))

        game.play_single_turn()

        self.assertEqual(2, len(game.other_player.minions))

        #Test Dispel option

        random.seed(1857)

        game = generate_game_for(KeeperOfTheGrove, StonetuskBoar, MinionPlayingAgent, MinionPlayingAgent)

        game.players[0].agent.choose_option = Mock(side_effect=lambda moonfire, dispel: dispel)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertTrue(game.current_player.minions[0].charge)

        game.play_single_turn()

        self.assertFalse(game.other_player.minions[0].charge)

        #Test when there are no targets for the spell
        random.seed(1857)
        game = generate_game_for(KeeperOfTheGrove, StonetuskBoar, MinionPlayingAgent, DoNothingBot)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(1, len(game.current_player.minions))
        self.assertEqual("Keeper of the Grove", game.current_player.minions[0].card.name)


    def test_DruidOfTheClaw(self):
        game = SavedGame("tests/replays/card_tests/DruidOfTheClaw.rep")
        game.start()
        self.assertEqual(0, len(game.current_player.minions))
        self.assertEqual(1, len(game.other_player.minions))
        self.assertEqual(4, game.other_player.minions[0].attack_power)
        self.assertEqual(6, game.other_player.minions[0].max_defense)
        self.assertEqual(2, game.other_player.minions[0].defense)
        self.assertTrue(game.other_player.minions[0].taunt)

    def test_Nourish(self):

        #Test gaining two mana
        game = generate_game_for(Nourish, StonetuskBoar, SpellTestingAgent, DoNothingBot)


        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(7, game.current_player.max_mana)
        self.assertEqual(7, len(game.current_player.hand))

        #Test drawing three cards
        random.seed(1857)
        game = generate_game_for(Nourish, StonetuskBoar, SpellTestingAgent, DoNothingBot)
        game.players[0].agent.choose_option = Mock(side_effect=lambda gain2, draw3: draw3)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(10, len(game.current_player.hand))
        self.assertEqual(5, game.current_player.max_mana)

    def test_Starfall(self):

        #Test gaining two mana
        game = generate_game_for(Starfall, StonetuskBoar, SpellTestingAgent, MinionPlayingAgent)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        self.assertEqual(4, len(game.current_player.minions))
        game.play_single_turn()

        self.assertEqual(0, len(game.other_player.minions))
        self.assertEqual(30, game.other_player.health)

        #Test drawing three cards
        random.seed(1857)
        game = generate_game_for(Starfall, MogushanWarden, SpellTestingAgent, MinionPlayingAgent)
        game.players[0].agent.choose_option = Mock(side_effect=lambda damageAll, damageOne: damageOne)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(1, len(game.other_player.minions))
        self.assertEqual(2, game.other_player.minions[0].defense)
        self.assertEqual(30, game.other_player.health)

    def test_ForceOfNature(self):
        game = generate_game_for(ForceOfNature, StonetuskBoar, SpellTestingAgent, DoNothingBot)
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        def check_minions():
            self.assertEqual(3, len(game.current_player.minions))

            for minion in game.current_player.minions:
                self.assertEqual(2, minion.attack_power)
                self.assertEqual(2, minion.defense)
                self.assertEqual(2, minion.max_defense)
                self.assertTrue(minion.charge)
                self.assertEqual("Treant", minion.card.name)

        game.other_player.bind_once("turn_ended", check_minions)

        game.play_single_turn()

        self.assertEqual(0, len(game.other_player.minions))

    def test_Starfire(self):
        game = generate_game_for(Starfire, MogushanWarden, EnemyMinionSpellTestingAgent, MinionPlayingAgent)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(2, len(game.current_player.minions))

        game.play_single_turn()

        self.assertEqual(2, len(game.other_player.minions))
        self.assertEqual(2, game.other_player.minions[0].defense)
        self.assertEqual(7, game.other_player.minions[1].defense)
        self.assertEqual(9, len(game.current_player.hand))

    def test_AncientOfLore(self):
        game = generate_game_for(AncientOfLore, Starfire, MinionPlayingAgent, EnemySpellTestingAgent)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        self.assertEqual(game.other_player.health, 25)

        game.play_single_turn()

        self.assertEqual(30, game.current_player.health)
        self.assertEqual(1, len(game.current_player.minions))
        self.assertEqual(5, game.current_player.minions[0].defense)
        self.assertEqual(5, game.current_player.minions[0].attack_power)
        self.assertEqual("Ancient of Lore", game.current_player.minions[0].card.name)

        random.seed(1857)

        game = generate_game_for(AncientOfLore, StonetuskBoar, MinionPlayingAgent, DoNothingBot)

        game.players[0].agent.choose_option = Mock(side_effect=lambda heal, draw: draw)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        self.assertEqual(10, len(game.current_player.hand))
        self.assertEqual(1, len(game.current_player.minions))
        self.assertEqual(5, game.current_player.minions[0].defense)
        self.assertEqual(5, game.current_player.minions[0].attack_power)
        self.assertEqual("Ancient of Lore", game.current_player.minions[0].card.name)

    def test_AncientOfWar(self):
        game = generate_game_for(AncientOfWar, IronbeakOwl, MinionPlayingAgent, MinionPlayingAgent)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(1, len(game.current_player.minions))
        self.assertEqual(5, game.current_player.minions[0].attack_power)
        self.assertEqual(10, game.current_player.minions[0].defense)
        self.assertEqual(10, game.current_player.minions[0].max_defense)
        self.assertTrue(game.current_player.minions[0].taunt)
        self.assertEqual("Ancient of War", game.current_player.minions[0].card.name)
        self.assertEqual(5, len(game.other_player.minions))

        game.play_single_turn()

        self.assertEqual(6, len(game.current_player.minions))
        self.assertEqual(5, game.other_player.minions[0].defense)
        self.assertEqual(5, game.other_player.minions[0].max_defense)
        self.assertFalse(game.other_player.minions[0].taunt)

        random.seed(1857)
        game = generate_game_for(AncientOfWar, IronbeakOwl, MinionPlayingAgent, MinionPlayingAgent)
        game.players[0].agent.choose_option = Mock(side_effect=lambda health, attack: attack)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(1, len(game.current_player.minions))
        self.assertEqual(10, game.current_player.minions[0].attack_power)
        self.assertEqual(5, game.current_player.minions[0].defense)
        self.assertEqual(5, game.current_player.minions[0].max_defense)
        self.assertFalse(game.current_player.minions[0].taunt)
        self.assertEqual("Ancient of War", game.current_player.minions[0].card.name)
        self.assertEqual(5, len(game.other_player.minions))

        game.play_single_turn()

        self.assertEqual(6, len(game.current_player.minions))
        self.assertEqual(5, game.other_player.minions[0].defense)
        self.assertEqual(5, game.other_player.minions[0].max_defense)
        self.assertEqual(5, game.other_player.minions[0].attack_power)
        self.assertFalse(game.other_player.minions[0].taunt)

    def test_IronbarkProtector(self):
        game = generate_game_for(IronbarkProtector, IronbeakOwl, MinionPlayingAgent, MinionPlayingAgent)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(1, len(game.current_player.minions))
        self.assertEqual(8, game.current_player.minions[0].attack_power)
        self.assertEqual(8, game.current_player.minions[0].defense)
        self.assertEqual(8, game.current_player.minions[0].max_defense)
        self.assertTrue(game.current_player.minions[0].taunt)
        self.assertEqual("Ironbark Protector", game.current_player.minions[0].card.name)
        self.assertEqual(6, len(game.other_player.minions))

        game.play_single_turn()

        self.assertEqual(7, len(game.current_player.minions))
        self.assertFalse(game.other_player.minions[0].taunt)


    def test_Cenarius(self):
        deck1 = StackedDeck([StonetuskBoar()], CHARACTER_CLASS.DRUID)
        deck2 = StackedDeck([WarGolem(), WarGolem(), Cenarius(), Cenarius()], CHARACTER_CLASS.DRUID)
        game = Game([deck1, deck2], [DoNothingBot(), MinionPlayingAgent()])
        game.pre_game()

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        self.assertEqual(2, len(game.other_player.minions))
        for minion in game.other_player.minions:
            self.assertEqual(7, minion.attack_power)
            self.assertEqual(7, minion.defense)
            self.assertEqual(7, minion.max_defense)
        game.play_single_turn()

        self.assertEqual(3, len(game.current_player.minions))

        self.assertEqual(5, game.current_player.minions[0].attack_power)
        self.assertEqual(8, game.current_player.minions[0].defense)
        self.assertEqual(8, game.current_player.minions[0].max_defense)
        self.assertEqual("Cenarius", game.current_player.minions[0].card.name)

        for minion_index in range(1, 3):
            minion = game.current_player.minions[minion_index]
            self.assertEqual(9, minion.attack_power)
            self.assertEqual(9, minion.defense)
            self.assertEqual(9, minion.max_defense)

        game.players[1].agent.choose_option = Mock(side_effect=lambda stats, summon: summon)

        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(6, len(game.current_player.minions))

        self.assertEqual(5, game.current_player.minions[0].attack_power)
        self.assertEqual(8, game.current_player.minions[0].defense)
        self.assertEqual(8, game.current_player.minions[0].max_defense)
        self.assertEqual("Cenarius", game.current_player.minions[0].card.name)

        self.assertEqual(2, game.current_player.minions[1].attack_power)
        self.assertEqual(2, game.current_player.minions[1].defense)
        self.assertEqual(2, game.current_player.minions[1].max_defense)
        self.assertTrue(game.current_player.minions[1].taunt)
        self.assertEqual("Treant", game.current_player.minions[1].card.name)

        self.assertEqual(2, game.current_player.minions[2].attack_power)
        self.assertEqual(2, game.current_player.minions[2].defense)
        self.assertEqual(2, game.current_player.minions[2].max_defense)
        self.assertTrue(game.current_player.minions[2].taunt)
        self.assertEqual("Treant", game.current_player.minions[2].card.name)

