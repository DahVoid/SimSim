"""Simulation."""
from time import sleep 
import cointainers
import resource
import nodes
from random import shuffle
import simsimui
from threading import Thread, Event, Lock



class Simulation:

    def __init__(self):
        # Gui
        self.gui = simsimui.SimSimsGUI(w=900, h=500)
        nodes.Node.gui = self.gui
        cointainers.Container.gui = self.gui
        resource.Resource.gui = self.gui
        # Simulation
        self.barn = cointainers.Barn()
        self.magazine = cointainers.Magazine()
        self.road = cointainers.Road()
        self.active = True
        nodes.Node.barn = self.barn
        nodes.Node.road = self.road
        nodes.Node.magazine = self.magazine
        self.factories = []
        self.fields = []
        self.flats = []
        self.dining_rooms = []
        self.all_trans = {}
        self.timer = Event()

        
        for _ in range(10):
            __worker = resource.Worker()
            self.road.insert_resource(__worker)
        
        for _ in range(2):
            self._add_node("Diner")
            self._add_node("Factory")
            self._add_node("Field")
            self._add_node("Flat")

    def refresh_all_trans(self):
        
        self.all_trans = []
        for node in self.factories:
            self.all_trans.append(node)
        for node in self.fields:
            self.all_trans.append(node)
        for node in self.dining_rooms:
            self.all_trans.append(node)
        for node in self.flats:
            self.all_trans.append(node)

    def adapt_nodes(self):
        """Adjust the amount of transistion in accordance to the amount of available resources."""
        #TODO calculate mean consumpiton and production per resource
        min_inv = 3
        max_inv = 20
        max_population = 15

        while self.active:

             # When all workers are gone stop the sim.
            if self.road.get_inventory() == 0:
                self.stop_sim()
                self.active = False
                break

            self.timer.wait(2)
            # Pause all trans
            for trans in self.all_trans:
                trans.event.clear()

            print("waiting to catch up")
            self.timer.wait(1)

            print("adapting")
            # Barn
            if self.barn.get_inventory() < min_inv:
                print("Adapt add farm")
                if len(self.dining_rooms) > 2:
                    self._remove_node("Diner")
                else:
                    self._add_node("Field")
            elif self.barn.get_inventory() > max_inv:
                print("Adapt remove farm")
                if len(self.fields) > 2:
                    self._remove_node("Field")
                else:
                    self._add_node("Diner")
            
            # Magazine 
            if self.magazine.get_inventory() < min_inv:
                print("Adapt add factory")
                self._add_node("Factory")
            elif self.magazine.get_inventory() > max_inv:
                print("Adapt remove factory")
                if len(self.factories) > 2:
                    self._remove_node("Factory")
                else:
                    #self._add_node("Flat")
                    for flat in self.flats:
                        if not flat.procreating:
                            flat.toggle_procreating(True)
                            break
                
            # Road 
            if self.road.get_inventory() < min_inv:
                print("add flat")
                for flat in self.flats:
                    if not flat.procreating:
                        flat.toggle_procreating(True)
                        break
                    elif len(self.flats) == self.flats.index(flat) + 1:
                        self._add_node("Flat")
                        break

            elif self.road.get_inventory() > max_population:
                print("remove flat")
                for flat in self.flats:
                    if flat.procreating:
                        flat.toggle_procreating(False)
                        break
                    elif len(self.flats) == self.flats.index(flat) + 1:
                        self._remove_node("Flat")
                        break


            self.start_gui()

            #Unpause all trans threads
            for trans in self.all_trans:
                trans.event.set()

    def stop_sim(self):
        for trans in self.all_trans:
            trans.event.set()
            trans.active = False
            for _ in self.flats:
                self._remove_node("Flat")
            for _ in self.dining_rooms:
                self._remove_node("Diner")
            for _ in self.fields:
                self._remove_node("Field")
            for _ in self.factories:
                self._remove_node("Factory")

    def start_gui(self):
        self.refresh_all_trans()
        self.barn.container_ui.autoplace(0, len(self.all_trans) + 3)
        self.road.container_ui.autoplace(1, len(self.all_trans) + 3)
        self.magazine.container_ui.autoplace(2, len(self.all_trans) + 3)
        for trans in self.all_trans:
            trans.node_ui.autoplace(self.all_trans.index(trans) + 3, len(self.all_trans) + 3)

    def update(self):
        """For each cycle update the priority list """

        self.refresh_all_trans()
        for node in self.all_trans:
            self.gui.update_ui()  
            node.update()
            if self.road.get_inventory() == 0:
                break
        
    def _add_node(self, trans_type):
        if trans_type == "Diner":
            trans = nodes.Dining_room()
            self.dining_rooms.append(trans)
            trans.start()
        elif trans_type == "Factory":
            trans = nodes.Factory()
            self.factories.append(trans)
            trans.start()
        elif trans_type == "Field":
            trans = nodes.Field()
            self.fields.append(trans)
            trans.start()
        elif trans_type == "Flat":
            trans = nodes.Flat()
            self.flats.append(trans)
            trans.start()
                
    def _remove_node(self, trans_type):
        if trans_type == "Diner" and len(self.dining_rooms) > 2:
            trans = self.dining_rooms[0]
            trans.event.set()
            trans.active = False
            trans.join()
            self.gui.remove(trans.node_ui)
            self.dining_rooms.remove(trans)
            del trans
            self.gui.update_ui()
        elif trans_type == "Factory" and len(self.factories) > 2:
            trans = self.factories[0]
            trans.event.set()
            trans.active = False
            trans.join()
            self.gui.remove(trans.node_ui)
            self.factories.remove(trans)
            del trans
            self.gui.update_ui()
        elif trans_type == "Field" and len(self.fields) > 2:
            trans = self.fields[0]
            trans.event.set()
            trans.active = False
            trans.join()
            self.gui.remove(trans.node_ui)
            self.fields.remove(trans)
            del trans
            self.gui.update_ui()
        elif trans_type == "Flat" and len(self.flats) > 2:
            trans = self.flats[0]
            trans.event.set()
            trans.active = False
            trans.join()
            self.gui.remove(trans.node_ui)
            self.flats.remove(trans)
            del trans
            self.gui.update_ui()


            
if __name__ == "__main__":
      
    sim = Simulation()
    sim.start_gui()
    i = 0
    t_adapt = Thread(target=sim.adapt_nodes, args=())
    t_adapt.start()
    input("Press Enter to quit.")
    t_adapt.join()
