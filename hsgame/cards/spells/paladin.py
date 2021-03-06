import hsgame.targetting
from hsgame.constants import CHARACTER_CLASS, CARD_RARITY
from hsgame.game_objects import Card, Minion, MinionCard, SecretCard

__author__ = 'Daniel'


class AvengingWrath(Card):
    def __init__(self):
        super().__init__("Avenging Wrath", 6, CHARACTER_CLASS.PALADIN, CARD_RARITY.COMMON, False)

    def use(self, player, game):
        super().use(player, game)
        for i in range(0, 8 + player.spell_power):
            targets = game.other_player.minions.copy()
            targets.append(game.other_player)
            target = targets[game.random(0, len(targets) - 1)]
            target.spell_damage(1, self)

class BlessedChampion(Card):
    def __init__(self):
        super().__init__("Blessed Champion", 5, CHARACTER_CLASS.PALADIN, CARD_RARITY.RARE, True, hsgame.targetting.find_minion_spell_target)
        
    def use(self, player, game):
        super().use(player, game)
        self.target.increase_attack(self.target.attack_power)
        
class BlessingOfKings(Card):
    def __init__(self):
        super().__init__("Blessing of Kings", 4, CHARACTER_CLASS.PALADIN, CARD_RARITY.COMMON, True, hsgame.targetting.find_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        self.target.increase_attack(4)
        self.target.increase_health(4)

class BlessingOfMight(Card):
    def __init__(self):
        super().__init__("Blessing of Might", 1, CHARACTER_CLASS.PALADIN, CARD_RARITY.FREE, True, hsgame.targetting.find_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        self.target.increase_attack(3)

class BlessingOfWisdom(Card):
    def __init__(self):
        super().__init__("Blessing of Wisdom", 1, CHARACTER_CLASS.PALADIN, CARD_RARITY.COMMON, True, hsgame.targetting.find_minion_spell_target)

    def use(self, player, game):

        def draw(*args):
            player.draw()

        super().use(player, game)
        self.target.bind("attack_minion", draw, self.target)
        self.target.bind("attack_player", draw, self.target)
        self.target.bind_once("silenced", lambda minion: minion.unbind("attack_minion", draw), self.target)
        self.target.bind_once("silenced", lambda minion: minion.unbind("attack_player", draw), self.target)

class Consecration(Card):
    def __init__(self):
        super().__init__("Consecration", 4, CHARACTER_CLASS.PALADIN, CARD_RARITY.COMMON, False)
        
    def use(self, player, game):
        super().use(player, game)
        for minion in game.other_player.minions.copy():
            minion.spell_damage(2 + player.spell_power, self)
        game.other_player.spell_damage(2 + player.spell_power, self)

class DivineFavor(Card):
    def __init__(self):
        super().__init__("Divine Favor", 3, CHARACTER_CLASS.PALADIN, CARD_RARITY.RARE, False)
        
    def use(self, player, game):
        super().use(player, game)
        while len(game.other_player.hand) > len(player.hand):
            player.draw()

class Equality(Card):
    def __init__(self):
        super().__init__("Equality", 2, CHARACTER_CLASS.PALADIN, CARD_RARITY.RARE, False)
        
    def use(self, player, game):
        super().use(player, game)
        
        targets = game.other_player.minions.copy()
        targets.extend(player.minions)
        
        for minion in targets:
            minion.decrease_health(minion.max_defense - 1)            
            
    def can_use(self, player, game):
        return super().can_use(player, game) and (len(player.minions) > 0 or len(game.other_player.minions) > 0)

class HammerOfWrath(Card):
    def __init__(self):
        super().__init__("Hammer of Wrath", 4, CHARACTER_CLASS.PALADIN, CARD_RARITY.FREE, True, hsgame.targetting.find_spell_target)
        
    def use(self, player, game):
        super().use(player, game)
        
        self.target.spell_damage(3 + player.spell_power, self)
        player.draw()

class HandOfProtection(Card):
    def __init__(self):
        super().__init__("Hand of Protection", 1, CHARACTER_CLASS.PALADIN, CARD_RARITY.FREE, True, hsgame.targetting.find_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        
        self.target.divine_shield = True
        
class HolyLight(Card):
    def __init__(self):
        super().__init__("Holy Light", 2, CHARACTER_CLASS.PALADIN, CARD_RARITY.FREE, True, hsgame.targetting.find_spell_target)

    def use(self, player, game):
        super().use(player, game)
        
        self.target.heal(6)
        
class HolyWrath(Card):
    def __init__(self):
        super().__init__("Holy Wrath", 5, CHARACTER_CLASS.PALADIN, CARD_RARITY.RARE, True, hsgame.targetting.find_spell_target)

    def use(self, player, game):
        super().use(player, game)
        
        player.draw()
        cost = player.hand[-1].mana
        self.target.spell_damage(cost + player.spell_power, self)

class Humility(Card):
    def __init__(self):
        super().__init__("Humility", 1, CHARACTER_CLASS.PALADIN, CARD_RARITY.COMMON, True, hsgame.targetting.find_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        
        # This will increase/decrease a minions attack to 1
        self.target.increase_attack(1 - self.target.attack_power)
        
class LayOnHands(Card):
    def __init__(self):
        super().__init__("Lay on Hands", 8, CHARACTER_CLASS.PALADIN, CARD_RARITY.EPIC, True, hsgame.targetting.find_spell_target)

    def use(self, player, game):
        super().use(player, game)
        
        self.target.heal(8)
        player.draw()
        player.draw()
        player.draw()

class EyeForAnEye(SecretCard):
    def __init__(self):
        super().__init__("Eye for an Eye", 1, CHARACTER_CLASS.PALADIN, CARD_RARITY.COMMON)

    def reveal(self, amount, what):
        what.player.damage(amount, self)
        super().reveal()

    def activate(self, player):
        player.bind_once("damaged", self.reveal)

    def deactivate(self, player):
        player.unbind("damaged", self.reveal)

class NobleSacrifice(SecretCard):
    def __init__(self):
        super().__init__("Noble Sacrifice", 1, CHARACTER_CLASS.PALADIN, CARD_RARITY.COMMON)

    def reveal(self, attacker):
        player = attacker.game.other_player
        
        if len(player.minions) < 7:
            class DefenderMinion(MinionCard):
                def __init__(self):
                    super().__init__("Defender", 1, CHARACTER_CLASS.PALADIN, CARD_RARITY.SPECIAL)

                @staticmethod
                def create_minion(player):
                    return Minion(2, 1)
    
            def choose_bender(targets):
                minion = DefenderMinion.create_minion(player)
                minion.add_to_board(DefenderMinion(), player.game, player, 0)
                player.game.current_player.agent.choose_target = old_target
                return minion
    
            old_target = player.game.current_player.agent.choose_target
            player.game.current_player.agent.choose_target = choose_bender
            super().reveal()
        else:
            self.activate(player)

    def activate(self, player):
        player.game.current_player.bind_once("attacking", self.reveal)

    def deactivate(self, player):
        player.game.current_player.unbind("attacking", self.reveal)
