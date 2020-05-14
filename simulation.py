"""Simulation"""
from time import sleep 
import cointainers
import resource
import nodes
from random import shuffle
import simsimui
import gui_obj

class Simulation:

    def __init__(self):
        # Gui
        self.gui = simsimui.SimSimsGUI(w=800, h=500)
        nodes.Node.gui = self.gui
        cointainers.Container.gui = self.gui
        resource.Resource.gui = self.gui
        # Simulation
        self.barn = cointainers.Barn()
        self.magazine = cointainers.Magazine()
        self.road = cointainers.Road()
        nodes.Node.barn = self.barn
        nodes.Node.road = self.road
        nodes.Node.magazine = self.magazine
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

        for _ in range(5):
            __worker = resource.Worker()
            self.road.insert_resource(__worker)
            self.road.container_ui.add_token(__worker.resource_ui)

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

    def stop_simulation(self):
        self.gui.shoot()

    def start_gui(self):
        self.barn.container_ui.autoplace(0, len(self.priority_list) + 3)
        self.road.container_ui.autoplace(1, len(self.priority_list) + 3)
        self.magazine.container_ui.autoplace(2, len(self.priority_list) + 3)
        self.refresh_priority_dict()
        for node in self.priority_list:
            node.node_ui.autoplace(self.priority_list.index(node) + 3, len(self.priority_list) + 3)

    def update(self):
        
        
        """For each cycle update the priority list """

        self.refresh_priority_dict()
        for node in self.priority_list:
            self.gui.update_ui()  
            node.update()
            if self.road.get_inventory() == 0:
                break
        
if __name__ == "__main__":
    
    total = 0
    for _ in range(100):
        i = 0
        sim = Simulation()


        sim.start_gui()
        sim.update()

        while sim.road.get_inventory() > 0:
            sim.update()
            
            i += 1
        print("Days/cycles completed: " + str(i))

        sim.stop_simulation()
        total += i
        current_avg = total/(_ + 1)
        print("Current avg: " + str(current_avg))

    input()