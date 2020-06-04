"""Cointains the classes responsible for producing resources."""
from resource import Food, Product, Worker
from time import sleep
from random import randint
from threading import Thread, Event

class Transition(Thread):
    """Superclass for producing classes."""

    barn = None
    road = None
    magazine = None
    gui = None
    
    def __init__(self, name, gui_properties):
        """Initialize the Transition."""
        super().__init__()
        Thread.__init__(self)
        self.event = Event()
        self.active = True
        self.name = name
        self._resources = []
        self._time_idle = 0
        self.transition_ui = self.gui.create_transition_ui(gui_properties)
        Transition.gui.connect(self.transition_ui, Transition.road.container_ui, {"arrows":True})
        Transition.gui.connect(Transition.road.container_ui, self.transition_ui, {"arrows":True})
    
    def run(self):
        """Until deactivated, run update(). Wait dictated in adapt method in Simulation."""
        while self.active:
            self.event.wait()
            self.update()
            Transition.gui.update_ui()

    def update(self):
        """Update the state of the transition."""
        raise NotImplementedError
    
    def produce(self):
        """Produce product."""
        raise NotImplementedError

    def consume_resources(self):
        """Consume the resources."""
        # We trust that our get_resource bring the correct ones.
        for item in self._resources:
            if not "Worker" in item.name:
                self.transition_ui.remove_token(item.resource_ui)
                Transition.gui.remove(item.resource_ui)
                self._resources.remove(item)
                del item
                Transition.gui.update_ui()
                
    def get_resource(self, resource_type):
        """Get a "Worker", "Food" or "Product" from their respective cointainer."""
        resource = None
        self.event.wait(0.2)
        if resource_type == "Worker":
            resource = Transition.road.get_resource()
            if resource:
                self._resources.append(resource)
                self.transition_ui.add_token(resource.resource_ui)
                Transition.gui.update_ui()
                return True
        elif resource_type == "Food":
            resource = Transition.barn.get_resource()
            if resource:
                self._resources.append(resource)
                self.transition_ui.add_token(resource.resource_ui)
                Transition.gui.update_ui()
                return True
        elif resource_type == "Product":
            resource = Transition.magazine.get_resource()
            if resource:
                self._resources.append(resource)
                self.transition_ui.add_token(resource.resource_ui)
                Transition.gui.update_ui()
                return True
        else:
            raise ValueError()   

        return False
        
    def return_resource(self, resource_type):
        """Return a local resource to it's respective container."""
        _resource = self.find_resource(resource_type)
        self.event.wait(0.2)
        if "Worker" in _resource.name:
            self.road.insert_resource(_resource)
            self.transition_ui.remove_token(_resource.resource_ui)
            Transition.gui.update_ui()
            
        elif "Food" in _resource.name:
            self.barn.insert_resource(_resource)
            self.transition_ui.remove_token(_resource.resource_ui)
            Transition.gui.update_ui()
            
        elif "Product" in _resource.name:
            self.magazine.insert_resource(_resource)
            self.transition_ui.remove_token(_resource.resource_ui)
            Transition.gui.update_ui()
            
        else:
            raise ValueError()
          
    def find_resource(self, resource_type):
        """Find a local resource by given string."""
        #todo  fix this so we dont have to return the worker
        for resource in self._resources:
            if resource_type in resource.name:
                self._resources.remove(resource)
                return resource

    def to_dict(self):
        """Return a dictionary with transition name and resources."""
        res_list = []
        for res in self._resources:
            res_list.append(res.to_dict())

        trans_dict = {
            "name": self.name,
            "resources": res_list
            }
        return trans_dict

    @staticmethod
    def create_from_dict(trans_dict):
        """Return a transition based upon parameter dict."""
        trans_name = trans_dict["name"]
        trans = None
        if "Dining_room" in trans_name:
            trans = Dining_room()
        elif "Factory" in trans_name:
            trans = Factory()
        elif "Field" in trans_name:
            trans = Field()
        elif "Flat" in trans_name:
            trans = Flat()
        
        for res_dict in trans_dict["resources"]:
            res_name = res_dict["name"]
            res = None
            if "Food" in res_name:
                res = Food.create_from_dict(res_dict)
                trans._resources.append(res)
                trans.transition_ui.add_token(res.resource_ui)
            elif "Product" in res_name:
                res = Product.create_from_dict(res_dict)
                trans._resources.append(res)
                trans.transition_ui.add_token(res.resource_ui)
            elif "Worker" in res_name:
                res = Worker.create_from_dict(res_dict)
                trans._resources.append(res)
                trans.transition_ui.add_token(res.resource_ui)

            Transition.gui.update_ui()

        return trans

class Factory(Transition):
    """Factory transition, produces a product when a worker is present."""

    _id = 0
    _gui_properties = {"lable":"Bryggeri", "color":"#ff0000", "fill":"#ffffff"}
    def __init__(self):
        """Create the Factory, assign id."""
        super().__init__("Factory" + str(Factory._id),Factory._gui_properties)
        Factory._id += 1
        Transition.gui.connect(self.transition_ui, Transition.magazine.container_ui, {"arrows":True})
    
    def produce(self, worker):
        """Create new produce and stores it locally."""
        # Don't subtract worker viability in event.wait in order to avoid dividing by 0.
        self.event.wait(1 + 10/worker.update_viability(0))
        worker.update_viability(-10)
        _produce = Product()
        self._resources.append(_produce)
        self.transition_ui.add_token(_produce.resource_ui)
        Transition.gui.update_ui()
        # Put back woker in inventory
        self._resources.append(worker)

    def random_accident(self, worker):
        """Oh boy here I go killing again."""
        if randint(1,10) == 1:
            worker.update_viability(-100)
 
    def update(self):
        """Run an update cycle on the factory."""
        if self.get_resource("Worker"):
            
            worker = self.find_resource("Worker")
            # Put back woker in inventory
            self._resources.append(worker)
            self.random_accident(worker)
            if worker.update_viability(0) < 1:
                self.return_resource("Worker")
                return
            else:
                self.produce(self.find_resource("Worker"))
                self.return_resource("Product")
                self.return_resource("Worker")
        else:
           self._time_idle += 1
        

class Field(Transition):
    """Field transition, produces food when a worker is present."""
    
    _id = 0
    _gui_properties = {"lable":"Rondellen Pizzeria", "color":"#00ff00", "fill":"#ffffff"}
    def __init__(self):
        """Create the Field, assign id."""
        super().__init__("Field" + str(Field._id), Field._gui_properties)
        Field._id += 1
        Transition.gui.connect(self.transition_ui, Transition.barn.container_ui, {"arrows":True})
    
    def random_accident(self, worker):
        """Oh boy here I go killing again."""
        if randint(1,15) == 1:
            worker.update_viability(-100)

    def produce(self, worker):
        """Create new produce."""
        _produce = Food()
        self._resources.append(_produce)
        self.transition_ui.add_token(_produce.resource_ui)
        Transition.gui.update_ui()
        self.random_accident(worker)
        # Put back worker to inventory
        self._resources.append(worker)

    def update(self):
        """Run an update cycle on the field."""
        if self.get_resource("Worker"):
            
            self.produce(self.find_resource("Worker"))
            self.return_resource("Food")
            self.return_resource("Worker")
        else:
           self._time_idle += 1
        

class Dining_room(Transition):
    """Dining_room transition, restores worker viability."""

    _id = 0
    _gui_properties = {"lable":"BTH", "color":"#555555", "fill":"#ffffff"}

    def __init__(self):
        """Create the Factory, assign id."""
        super().__init__("Dining_room" + str(Dining_room._id), Dining_room._gui_properties)
        Dining_room._id += 1
        Transition.gui.connect(Transition.barn.container_ui, self.transition_ui, {"arrows":True})

    def produce(self, worker):
        """Create new produce."""
        self.consume_resources()
        food_value = randint(10, 40)

        if self.random_accident():
            worker.update_viability(-food_value)
        else:
            worker.update_viability(food_value)
        
        # Put back worker to inventory
        self._resources.append(worker)
        
    def random_accident(self):
        """Oh boy here I go killing again."""
        if randint(1,20) == 1:
            return True
        else:
             return False

    def update(self):
        """Run an update cycle on the dining room."""
        if self.get_resource("Worker"):
            if self.get_resource("Food"):
                self.produce(self.find_resource("Worker"))
                self.return_resource("Worker")
            else:
                self.return_resource("Worker")
        else:
            self._time_idle += 1
    

class Flat(Transition):
    """Flat transition, restores worker viability."""

    _id = 0
    _gui_properties = {"lable":"Lokalen™", "color":"#00c993", "fill":"#000000"}

    def __init__(self):
        """Create the Flat, assign id."""
        super().__init__("Flat" + str(Flat._id), Flat._gui_properties)
        Flat._id += 1
        Transition.gui.connect(Transition.magazine.container_ui, self.transition_ui,{"arrows":True})
        self.procreating = True

    def rest(self, worker):
        """Create new produce."""
        self.consume_resources()
        worker.update_viability(randint(10, 60))
        # Put back worker to inventory
        self._resources.append(worker)
    
    def reprocreate(self):
        """Create new worker."""
        _child = Worker()
        self._resources.append(_child)
        self.transition_ui.add_token(_child.resource_ui)
        Transition.gui.update_ui()

    def toggle_procreating(self, procreate):
        """Enter wether a flat should procreate or not."""
        if procreate:
            self.procreating = False
        else:
            self.procreating = True

    def update(self):
        """Run an update cycle on the dining room."""
        self.get_resource("Product")
        self.get_resource("Worker")
        if self.procreating:
            self.get_resource("Worker")

        if (len(self._resources) == 2 and not self.procreating) or (len(self._resources) == 3 and self.procreating):
            if len(self._resources) == 3:
                self.consume_resources()
                self.reprocreate()
                self.return_resource("Worker")
                self.return_resource("Worker")
                self.return_resource("Worker")
            else:
                self.consume_resources()
                self.rest(self.find_resource("Worker"))
                self.return_resource("Worker")
        else:
            while len(self._resources) > 0:
                if "Worker" in self._resources[0].name:
                    self.return_resource("Worker")
                else:
                    self.return_resource("Product")
                
            self._time_idle += 1
    