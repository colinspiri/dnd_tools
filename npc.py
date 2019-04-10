from creature import Creature
import constants

class NPC(Creature):
    def __init__(self, name, max_health, ability_scores):
        Creature.__init__(self, name)
        self.max_health = max_health
        self.current_health = self.max_health

        self.ability_scores = ability_scores
        self.ability_modifiers = {}
        for ability, score in self.ability_scores.items():
            self.ability_modifiers[ability] = constants.ABILITY_MODIFIERS[score]

    def __str__(self):
        return self.name + " has " + str(self.current_health) + "/" + str(self.max_health) + " health."

if __name__ == "__main__":
    npc = NPC("bob", 20, 10, {
    'STR': 10,
    'DEX': 12,
    'CON': 14,
    'INT': 6,
    'WIS': 9,
    'CHA': 15
    })
