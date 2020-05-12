"""Simulation"""

import cointainers
import resource
import nodes
from random import shuffle

class Simulation:

    def __init__(self):

        self.barn = cointainers.Barn()
        self.magazine = cointainers.Magazine()
        self.road = cointainers.Road()
        self.factories = []
        self.fields = []
        self.flats = []
        self.dining_rooms = []
        self.priority_list = {}
        for _ in range(2):
            self.dining_rooms.append(nodes.Dining_room())
            self.factories.append(nodes.Factory())
            self.fields.append(nodes.Field())
            self.flats.append(nodes.Flat())

        nodes.Node.barn = self.barn
        nodes.Node.road = self.road
        nodes.Node.magazine = self.magazine

        for _ in range(5):
            self.road.insert_resource(resource.Worker())

    def refresh_priority_dict(self):
        self.priority_list = []
        for node in self.factories:
            self.priority_list.append(node)
        for node in self.fields:
            self.priority_list.append(node)
        for node in self.dining_rooms:
            self.priority_list.append(node)
        for node in self.flats:
            self.priority_list.append(node)
        
        shuffle(self.priority_list)

    def update(self):
        """For each cycle update the priority list """
        self.refresh_priority_dict()
        for node in self.priority_list:
            node.update()
        
if __name__ == "__main__":
    sim = Simulation()

    i = 0

    while i < 50000:
        sim.update()
        i += 1