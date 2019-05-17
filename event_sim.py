"""
    File: event_sim.py
    Author: Cole Blakley
    Purpose: A module containing code to make Markov chain-based simulations.
        By creating Agents (objects that run/store data of a sim) and defining
        start(), update(), and end() functions to be passed into a SimKit (an
        object containing logic specific to the current simulation), as well as
        defining states/transitions in a JSON file, event simulations can
        be run, with user-given probabilites used to choose each transition.
"""
import json, sys, random

class EventType:
    """Purpose: A kind of event that can occur during a simulation"""
    def __init__(self, name):
        """Creates a new type of event with a given name and blank attributes"""
        self.name = name
        self.description = ""
        self.suffixes = []
        #chances contains likelihood of corresponding suffix event occurring
        self.chances = []

    def step(self):
        """Advance the simulation by choosing the next event from the available
            suffix events using their weighted probabilities"""
        if len(self.suffixes) > 0:
            return random.choices(self.suffixes, weights=self.chances)[0]

    def __str__(self):
        return "Name: {} Description: {} Suffixes: {}\n".format(self.name, self.description,
                                                                self.suffixes)

class SimKit:
    """Purpose: A group of functions called during/after a simulation. This is
        where the unique logic of each sim belongs"""
    def __init__(self, start_func, update_func, end_func):
        """Creates new SimKit, accepting three functions"""
        self.start_func = start_func
        self.update_func = update_func
        self.end_func = end_func

    def start(self, data):
        """Function called before sim begins"""
        self.start_func(data)

    def update(self, data, event):
        """Function called after every event occurs"""
        self.update_func(data, event)

    def end(self, agent, data):
        """Function called after the simulation ends"""
        self.end_func(agent, data)

class Agent:
    """Purpose: Supervises the sim. Keeps track of data in simulation, using
        code in the given sim kit."""
    def __init__(self, name, event_types):
        """Creates a new agent that references a given list of event types."""
        self.name = name
        self.event_types = event_types #All the possible events in the sim
        self.data = {} #State accumulated during run() of sim
        self.log = []

    def run(self, sim_kit, limit):
        """Run the simulation starting with the root event. Stop after end event (when
            event is None), log the events that occur, and if necessary, stop after limit
            amount of events."""
        event = self.event_types["root"]
        sim_kit.start(self.data)
        for i in range(limit):
            if event == None:
                #event will be None right after end event is called
                print("Simulation complete.")
                break
            #Sim kit executes some code after each event
            sim_kit.update(self.data, event)
            self.log.append(event.name)
            #Continue on to next event
            event = event.step()
        #Do specified end procedure (usually means displaying data about sim)
        sim_kit.end(self, self.data)

def load_event_types(path):
    """Read a JSON file and load the event types specified within it into
        EventType objects"""
    try:
        json_file = open(path)
    except IOError:
        print("Error: Can't load", path)
        sys.exit(1)
    json_file.seek(0)
    event_type_specs = json.load(json_file)["event_types"]
    json_file.close()
    event_types = {}
    #Add all specs to dict, initially with only basic info specified
    for spec in event_type_specs:
        new_type = EventType(spec["name"])
        new_type.description = spec["description"]
        event_types[spec["name"]] = new_type
    #Finish creation by linking event_types to event_types that are suffixes
    for spec in event_type_specs:
        curr_type = event_types[spec["name"]]
        for suffix_name, chance in spec["suffixes"].items():
            try:
                new_suffix = event_types[suffix_name]
            except KeyError:
                print("Error: Unknown suffix name", suffix_name)
                sys.exit(1)
            curr_type.suffixes.append(new_suffix)
            curr_type.chances.append(chance)
        #Validate probabilities of suffixes; can have empty suffix dict; otherwise,
        #total of probabilities must be 100%
        if sum(curr_type.chances) != 100 and len(curr_type.chances) != 0:
            print("Error: Chances for", curr_type.name, "'s suffixes don't sum to 100%")
            sys.exit(1)
    return event_types
