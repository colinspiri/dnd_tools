import initiative as init
import dice
import jsonloader as loader

def get_input(initiative):
    text = input("> ").strip()
    if len(text) == 0:
        print("Invalid input. Try again, but with words this time.")
    else:
        process_input(initiative, text)

def process_input(initiative, text):
    text_elements = text.strip().split()
    command = text_elements[0]
    text_elements.remove(command)
    run_command(initiative, command, text_elements)

def run_command(initiative, command, components):
    if command == "next":
        command_next(initiative)
    elif command == "end":
        command_end(initiative)
    elif command == "roll":
        command_roll(components)
    elif command == "damage":
        command_damage(initiative, components)
    elif command == "heal":
        command_heal(initiative, components)
    elif command == "remove":
        command_remove(initiative, components)
    elif command == "action":
        command_action(initiative, components)
    elif command == "save":
        command_save(initiative, components)
    elif command == "check":
        command_check(initiative, components)
    elif command == "help":
        command_help(components)
    else:
        print("Command not recognized. Type \'help\' for a list of available commands.")

def command_next(initiative):
    initiative.next_turn()
def command_end(initiative):
    pcs_to_update = []
    for set in initiative.order:
        if hasattr(set["entity"], "json_object"):
            pcs_to_update.append(set["entity"])
    if len(pcs_to_update) > 0:
        loader.update_pcs(pcs_to_update)
    print("Program ended.")
    quit()
def command_roll(components):
    if len(components) == 0:
        print("Invalid input. Roll command requires more parameters.")
        return
    # Roll attack
    elif components[0] == "attack":
        dice.show_attack(components[1], components[2])
    # Roll save
    elif components[0] == "save":
        dice.show_save(components[1], components[2])
    # Roll DICE
    else:
        dice.show_roll("".join(components))
def command_damage(initiative, components):
    if len(components) == 0:
        print("Invalid input. Damage command requires more parameters.")
        return
    elif len(components) == 1:
        damage_amount = components[0]
        if not damage_amount.isdigit():
            _, _, damage_amount = dice.show_roll(damage_amount)
        initiative.damage_current_entity(int(damage_amount))
    else:
        name = components[0]
        damage_amount = components[1]
        if not damage_amount.isdigit():
            _, _, damage_amount = dice.show_roll(damage_amount)
        initiative.damage_entity(initiative.get_entity(name), int(damage_amount))
def command_heal(initiative, components):
    if len(components) == 0:
        print("Invalid input. Heal command requires more parameters.")
        return
    elif len(components) == 1:
        heal_amount = components[0]
        if not heal_amount.isdigit():
            _, _, heal_amount = dice.show_roll(heal_amount)
        initiative.damage_current_entity(-1*int(heal_amount))
    else:
        name = components[0]
        heal_amount = components[1]
        if not heal_amount.isdigit():
            _, _, heal_amount = dice.show_roll(heal_amount)
        initiative.damage_entity(initiative.get_entity(name), -1*int(heal_amount))
def command_remove(initiative, components):
    if len(components) == 0:
        initiative.get_current_entity().dead = True
    # Remove INDEX
    else:
        initiative.order[int(components[0])]["creature"].dead = True
    initiative.remove_dead_entities()
def command_action(initiative, components):
    creature = initiative.get_current_entity()
    if len(components) == 0:
        creature.show_actions()
    # Action ACTION_NAME
    else:
        creature.action(components[0])
def command_save(initiative, components):
    if len(components) == 0:
        print("Invalid input. Save command requires more parameters.")
        return
    entity = initiative.get_current_entity()
    if not hasattr(entity, "saving_throws"):
        print(entity.name + " cannot roll a saving throw. Did you want a d20 roll?")
        dice.show_roll("d20")
        return
    ability = components[0].upper()
    save_dc = None
    if len(components) == 2:
        save_dc = components[1]
    try:
        entity.save(ability, save_dc)
    except:
        if save_dc is None:
            print(entity.name + " has no saving throw named \'" + ability + "\'.")
        else:
            print("\'" + ability + "\' and \'" + save_dc + "\' not recognized as valid input for ABILITY and SAVE DC.")
def command_check(initiative, components):
    if len(components) == 0:
        print("Invalid input. Check command requires more parameters.")
        return
    entity = initiative.get_current_entity()
    if not hasattr(entity, "skills"):
        print(entity.name + " cannot roll a skill check. Did you want a d20 roll?")
        dice.show_roll("d20")
        return
    skill = "_".join(components).lower()
    try:
        entity.skill_check(skill)
    except:
        print(entity.name + " has no skill or ability named \'" + skill + "\'.")
def command_help(components):
    if len(components) == 0:
        commands = loader.get_command_names()
        print("Here's a list of available commands: " + str(commands))
    else:
        print(loader.get_command_description(components[0]))
