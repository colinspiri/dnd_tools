from creature import Creature
import constants
import dice
import jsonloader as loader

class NPC(Creature):
    def __init__(self, object):
        Creature.__init__(self, object["name"])
        rolls, modifier, result = dice.roll(object["max_health"])
        self.max_health = result
        self.current_health = self.max_health
        self.armor_class = object["armor_class"]

        # Ability scores
        self.ability_scores = object["ability_scores"]
        self.ability_modifiers = {}
        for ability, score in self.ability_scores.items():
            self.ability_modifiers[ability] = constants.ABILITY_MODIFIERS[score]

        # Saving throws
        self.saving_throws = self.ability_modifiers.copy()
        for ability, modifier in object["saving_throws"].items():
            self.saving_throws[ability] = modifier

        self.actions = object["actions"]

    def action(self, requested_action):
        for action_name, action in self.actions.items():
            # Check actual action name
            if action_name == requested_action:
                self.execute_action(action)
                return
            # Check commands also
            try:
                for command in action["commands"]:
                    if command == requested_action:
                        self.execute_action(action)
                        return
            except:
                pass
        print("Action name not recognized.")
    def execute_action(self, action):
        # Get to hit and damage amounts
        to_hit = action["to_hit"]
        damages = action["damage"]
        basic_damage_dice = action["damage"][0]["damage_dice"]
        basic_damage_type = action["damage"][0]["damage_type"]

        # Show summary of action
        summary = self.name + " attacks with " + to_hit + " to hit and deals " + basic_damage_dice + " " + basic_damage_type + " damage"
        for i in range(1, len(damages)):
            summary += " and " + damages[i]["damage_dice"] + " " + damages[i]["damage_type"] + " damage"
        print(summary + ".")

        # Show attack with basic damage
        critical = dice.show_attack(to_hit, basic_damage_dice, basic_damage_type)[2]

        # If critical failure, don't show extra damage
        if critical == False:
            return
        # If more damage in array, show bonus damage
        for i in range(1, len(damages)):
            damage_tuple = dice.roll(damages[i]["damage_dice"])
            damage_result = damage_tuple[2]
            print("Bonus Damage: " + str(damage_result) + " (" + damages[i]["damage_type"] + ")")
        # Show effects
        for i in range(len(action["effects"])):
            print("-" + action["effects"][i])
        return

    def save(self, ability, save_dc):
        save_bonus = self.saving_throws[ability]
        save_success, saving_throw = dice.show_save(str(save_bonus), save_dc)
        return save_success, saving_throw

    def __str__(self):
        return self.name + " has " + str(self.current_health) + "/" + str(self.max_health) + " health."

if __name__ == "__main__":
    npc = NPC(loader.get_creature("wolf"))
    print(npc)
    npc.action("bite")
