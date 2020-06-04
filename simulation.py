"""Simulation."""
from time import sleep 
import cointainers
import resource
import transitions
from random import shuffle
import simsimui
from threading import Thread, Event, Lock
import json



class Simulation:
    """Contains everything to needed to run the a simulation."""

    def __init__(self, new_sim):
        """Create a sim, new_sim parameter dictates wether creating a new sim or loading saved."""
        # Gui
        self.gui = simsimui.SimSimsGUI(w=900, h=500)
        transitions.Transition.gui = self.gui
        cointainers.Container.gui = self.gui
        resource.Resource.gui = self.gui
        # Simulation
        self.barn = None
        self.magazine = None
        self.road = None
        if not new_sim:
            self.barn = cointainers.Barn()
            self.magazine = cointainers.Magazine()
            self.road = cointainers.Road()
        self.active = True
        transitions.Transition.barn = self.barn
        transitions.Transition.road = self.road
        transitions.Transition.magazine = self.magazine
        self.factories = []
        self.fields = []
        self.flats = []
        self.dining_rooms = []
        self.all_trans = {}
        self.timer = Event()

        if not new_sim:
            for _ in range(10):
                __worker = resource.Worker()
                self.road.insert_resource(__worker)
            
            for _ in range(2):
                self._add_transition("Diner")
                self._add_transition("Factory")
                self._add_transition("Field")
                self._add_transition("Flat")

    def refresh_all_trans(self):
        """Refresh all_trans list, removes old and adds new transitions."""        
        self.all_trans = []
        for transition in self.factories:
            self.all_trans.append(transition)
        for transition in self.fields:
            self.all_trans.append(transition)
        for transition in self.dining_rooms:
            self.all_trans.append(transition)
        for transition in self.flats:
            self.all_trans.append(transition)

    def adapt_transitions(self):
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
                    self._remove_transition("Diner")
                else:
                    self._add_transition("Field")
            elif self.barn.get_inventory() > max_inv:
                print("Adapt remove farm")
                if len(self.fields) > 2:
                    self._remove_transition("Field")
                else:
                    self._add_transition("Diner")
            
            # Magazine 
            if self.magazine.get_inventory() < min_inv:
                print("Adapt add factory")
                self._add_transition("Factory")
            elif self.magazine.get_inventory() > max_inv:
                print("Adapt remove factory")
                if len(self.factories) > 2:
                    self._remove_transition("Factory")
                else:
                    #self._add_transition("Flat")
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
                        self._add_transition("Flat")
                        break

            elif self.road.get_inventory() > max_population:
                print("remove flat")
                for flat in self.flats:
                    if flat.procreating:
                        flat.toggle_procreating(False)
                        break
                    elif len(self.flats) == self.flats.index(flat) + 1:
                        self._remove_transition("Flat")
                        break


            self.start_gui()

            self.save_sim()
            #Unpause all trans threads
            for trans in self.all_trans:
                trans.event.set()

    def stop_sim(self):
        """Let the trans finish run, then deactive and remove them."""
        for trans in self.all_trans:
            trans.event.set()
            trans.active = False
            for _ in self.flats:
                self._remove_transition("Flat")
            for _ in self.dining_rooms:
                self._remove_transition("Diner")
            for _ in self.fields:
                self._remove_transition("Field")
            for _ in self.factories:
                self._remove_transition("Factory")

    def start_gui(self):
        """Auto place all the ui components."""
        self.refresh_all_trans()
        self.barn.container_ui.autoplace(0, len(self.all_trans) + 3)
        self.road.container_ui.autoplace(1, len(self.all_trans) + 3)
        self.magazine.container_ui.autoplace(2, len(self.all_trans) + 3)
        for trans in self.all_trans:
            trans.transition_ui.autoplace(self.all_trans.index(trans) + 3, len(self.all_trans) + 3)

    def update(self):
        """For each cycle update the priority list."""
        self.refresh_all_trans()
        for transition in self.all_trans:
            self.gui.update_ui()  
            transition.update()
            if self.road.get_inventory() == 0:
                break
        
    def _add_transition(self, trans_type):
        if trans_type == "Diner":
            trans = transitions.Dining_room()
            self.dining_rooms.append(trans)
            trans.start()
        elif trans_type == "Factory":
            trans = transitions.Factory()
            self.factories.append(trans)
            trans.start()
        elif trans_type == "Field":
            trans = transitions.Field()
            self.fields.append(trans)
            trans.start()
        elif trans_type == "Flat":
            trans = transitions.Flat()
            self.flats.append(trans)
            trans.start()
                
    def _remove_transition(self, trans_type):
        if trans_type == "Diner" and len(self.dining_rooms) > 2:
            trans = self.dining_rooms[0]
            trans.event.set()
            trans.active = False
            trans.join()
            self.gui.remove(trans.transition_ui)
            self.dining_rooms.remove(trans)
            del trans
            self.gui.update_ui()
        elif trans_type == "Factory" and len(self.factories) > 2:
            trans = self.factories[0]
            trans.event.set()
            trans.active = False
            trans.join()
            self.gui.remove(trans.transition_ui)
            self.factories.remove(trans)
            del trans
            self.gui.update_ui()
        elif trans_type == "Field" and len(self.fields) > 2:
            trans = self.fields[0]
            trans.event.set()
            trans.active = False
            trans.join()
            self.gui.remove(trans.transition_ui)
            self.fields.remove(trans)
            del trans
            self.gui.update_ui()
        elif trans_type == "Flat" and len(self.flats) > 2:
            trans = self.flats[0]
            trans.event.set()
            trans.active = False
            trans.join()
            self.gui.remove(trans.transition_ui)
            self.flats.remove(trans)
            del trans
            self.gui.update_ui()

    def save_sim(self):
        """Convert sim state to dict."""
        trans_list = []
        for trans in self.all_trans:
            trans_list.append(trans.to_dict())
        cont_list = []
        cont_list.append(self.road.to_dict())
        cont_list.append(self.magazine.to_dict())
        cont_list.append(self.barn.to_dict())
        sim_dict = {
            "transitions": trans_list,
            "containers": cont_list
        }

        #Save JSON locally
        with open("json_data.txt", "w") as outfile:
            json.dump(sim_dict, outfile)
          
if __name__ == "__main__":

    if input("Want to load old sim? (y/n): ") == "y":
        print("Last autosave file name: json_data.txt")
        with open(input("Enter file name: ")) as json_file:
            data = json.load(json_file)

        sim = Simulation(True)
        

        factories = []
        fields = []
        flats = []
        dining_rooms = []
        road = None
        magazine = None
        barn = None            

        for cont_dict in data["containers"]:
            cont = cointainers.Container.create_from_dict(cont_dict)
            if "Magazine" in cont.name:
                magazine = cont
            elif "Barn" in cont.name:
                barn = cont
            elif "Road" in cont.name:
                road = cont

        sim.road = road
        sim.magazine = magazine
        sim.barn = barn
        transitions.Transition.barn = sim.barn
        transitions.Transition.road = sim.road
        transitions.Transition.magazine = sim.magazine

        for trans_dict in data["transistions"]:
            trans = transitions.Transition.create_from_dict(trans_dict)
            if "Factory" in trans.name:
                factories.append(trans)
            elif "Field" in trans.name:
                fields.append(trans)
            elif "Flat" in trans.name:
                flats.append(trans)
            elif "Dining_room" in trans.name:
                dining_rooms.append(trans)
        
        sim.factories = factories
        sim.fields = fields
        sim.flats = flats
        sim.dining_rooms = dining_rooms
       
        sim.refresh_all_trans()

        for trans in sim.all_trans:
            trans.start()
        sim.start_gui()

    else:
        sim = Simulation(False)
        sim.start_gui()
    
    t_adapt = Thread(target=sim.adapt_transitions, args=())
    t_adapt.start()

    input("Press Enter to quit.")
    t_adapt.join()
