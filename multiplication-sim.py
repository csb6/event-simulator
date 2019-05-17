"""
    File: multiplication-sim.py
    Author: Cole Blakley
    Purpose: Multiplies 10 by an amount determined by a Markov chain. After a
        50/50 chance of adding 10 or 20, there is a 45% chance each event to add
        10 or 20, with a 10% chance of the simulation stopping. Max possible sum is
        600 using a upper limit of 30 total events. Depends on mulitplication-sim.json
        for the specifications of each state/transition. Intended to be a simple (and
        not very useful) example to show what bare-bones sim looks like.
"""
import event_sim

def start(data):
    data["sum"] = 0

def update(data, event):
    if event.name == "add_10":
        data["sum"] += 10
    elif event.name == "add_20":
        data["sum"] += 20

    print(event.description)

def end(agent, data):
    print("\n\nSUMMARY:\n")
    print("In total, 10 was multiplied {} times by the simulation".format(data["sum"] // 10))

def main():
    event_types = event_sim.load_event_types("multiplication-sim.json")
    runner = event_sim.Agent("Runner", event_types)
    multiplcation_sim = event_sim.SimKit(start, update, end)
    runner.run(multiplcation_sim, 30)

main()
