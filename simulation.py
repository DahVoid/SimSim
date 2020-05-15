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
        # todo prioritize flats if needed 

    def adapt_nodes(self):
        _min_inv = 3
        _max_inv = 20
        # Barn
        if self.barn.get_inventory() < _min_inv:
            if len(self.dining_rooms) > 2:
                self._remove_node("Diner")
            else:
                self._add_node("Field")
        elif self.barn.get_inventory() > _max_inv:
            if len(self.fields) > 2:
                self._remove_node("Field")
            else:
                self._add_node("Diner")
        
        # Magazine 
        if self.magazine.get_inventory() < _min_inv:
            
            self._add_node("Factory")
        elif self.magazine.get_inventory() > _max_inv:
            if len(self.factories) > 2:
                self._remove_node("Factory")
            else:
                self._add_node("Flat")
            
        # Road 
        if self.road.get_inventory() < _min_inv:
            for flat in self.flats:
                if not flat.procreating:
                    flat.toggle_procreating(True)
                    break
                elif len(self.flats) == self.flats.index(flat) + 1:
                    self._add_node("Flat")
                    break

        elif self.road.get_inventory() > _max_inv:
            for flat in self.flats:
                if flat.procreating:
                    flat.toggle_procreating(False)
                    break
                elif len(self.flats) == self.flats.index(flat) + 1:
                    self._remove_node(flat)
                    break
        
        # Check surplus

        # act on surplus

    def stop_gui(self):
        self.gui.shoot()

    def start_gui(self):
        self.refresh_priority_dict()
        self.barn.container_ui.autoplace(0, len(self.priority_list) + 3)
        self.road.container_ui.autoplace(1, len(self.priority_list) + 3)
        self.magazine.container_ui.autoplace(2, len(self.priority_list) + 3)
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
        
    def _add_node(self, trans_type):
        if trans_type == "Diner":
            self.dining_rooms.append(nodes.Dining_room())
        elif trans_type == "Factory":
            self.factories.append(nodes.Factory())
        elif trans_type == "Field":
            self.fields.append(nodes.Field())
        elif trans_type == "Flat":
            self.flats.append(nodes.Flat())
        
        self.start_gui()
        
    def _remove_node(self, trans_type):
        if trans_type == "Diner" and len(self.dining_rooms) > 0:
            trans = self.dining_rooms[0]
            self.gui.remove(trans.node_ui)
            self.dining_rooms.remove(trans)
            del trans
            self.gui.update_ui()
        elif trans_type == "Factory" and len(self.factories) > 0:
            trans = self.factories[0]
            self.gui.remove(trans.node_ui)
            self.factories.remove(trans)
            del trans
            self.gui.update_ui()
        elif trans_type == "Field" and len(self.fields) > 0:
            trans = self.fields[0]
            self.gui.remove(trans.node_ui)
            self.fields.remove(trans)
            del trans
            self.gui.update_ui()
        elif trans_type == "Flat" and len(self.flats) > 0:
            trans = self.flats[0]
            self.gui.remove(trans.node_ui)
            self.flats.remove(trans)
            del trans
            self.gui.update_ui()
        self.start_gui()
        
            
            

if __name__ == "__main__":
      
    sim = Simulation()

    sim.start_gui()
    sim.update()
    i = 1
    while sim.road.get_inventory() > 0:
        sim.update()
        if i % 5:
            sim.adapt_nodes()
        
        i += 1
        print("Days survived: " + str(i))
    print("Days/cycles completed: " + str(i))

    sim.stop_gui()
