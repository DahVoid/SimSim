"""Simulation"""

import cointainers
from resource import Worker
import nodes

class Simulation:

    def __init__(self):

        self.barn = cointainers.Barn
        self.magazine = cointainers.Magazine
        self.road = cointainers.Road
        self.factories = []
        self.fields = []
        self.flats = []
        self.dining_rooms = []

        for _ in range(2):
            self.dining_rooms.append(nodes.Dining_room())
            self.factories.append(nodes.Factory())
            self.fields.append(nodes.Field())
            self.flats.append(nodes.Flat())

            nodes.Node.barn = self.barn
            nodes.Node.road = self.road
            nodes.Node.Magazine = self.magazine

