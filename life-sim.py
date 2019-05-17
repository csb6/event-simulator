"""
    File: life-sim.py
    Author: Cole Blakley
    Purpose: Contains function definitions for sim kit that simulates a
        person's life as a series of states (e.g. gets sicks, cries, is born).
        Depends on states defined in life-sim.json. Creates Agent object named
        "Tom" that runs the sim, printing out the description of each event
        and a short summary of stats after the sim finishes.
"""
import event_sim

def start(data):
    #Run just before sim starts
    data["days_alive"] = 0
    data["times_cried"] = 0
    data["days_sick"] = 0
    data["sleepless_nights"] = 0

def update(data, event):
    #Run after each event occurs
    if event.name == "get_name":
        data["name"] = input("Enter a name: ")
    elif event.name == "name_is_boy":
        data["sex"] = "male"
    elif event.name == "name_is_girl":
        data["sex"] = "female"
    elif event.name == "name_is_american":
        data["nationality"] = "american"
    elif event.name == "name_is_canadian":
        data["nationality"] = "canadian"
    elif event.name == "day_passes":
        data["days_alive"] += 1
    elif event.name == "name_gets_sick":
        data["days_sick"] += 1
    elif event.name == "name_can't_sleep":
        data["sleepless_nights"] += 1
    elif event.name == "name_cries":
        data["times_cried"] += 1

    #Print out the update
    print(event.description)

def end(agent, data):
    #Run after sim completes
    print("\n\nSUMMARY:")
    print("Agent {} simulated the life of {}.".format(agent.name, data["name"]))
    print("Here are {}'s stats:".format(data["name"]))
    for field, value in data.items():
        print(" {}: {}".format(field, value))

def main():
    event_types = event_sim.load_event_types("life-sim.json")
    tom = event_sim.Agent("Tom", event_types)
    life_sim = event_sim.SimKit(start, update, end)
    #Simulate (at most) 500 events in a person's life
    tom.run(life_sim, 500)

main()
