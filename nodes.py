"""Cointains the classes responsible for producing resources."""
from resource import Food, Product, Worker
from time import sleep
from random import randint

class Node():
    """Superclass for producing classes."""

    barn = None
    road = None
    magazine = None
    gui = None

    def __init__(self, name, gui_properties):
        """Initialize the Node."""
        super().__init__()
        self.name = name
        self._resources = []
        self._time_idle = 0
        self.node_ui = self.gui.create_transition_ui(gui_properties)
        Node.gui.connect(self.node_ui, Node.road.container_ui, {})
        Node.gui.connect(Node.road.container_ui, self.node_ui, {})
    
    def update(self):
        """Update the state of the node."""
        raise NotImplementedError
    
    def produce(self):
        """Produce product."""
        raise NotImplementedError

    def consume_resources(self):
        """Consume the resources."""
        # We trust that our get_resource bring the correct ones.
        for item in self._resources:
            if not "Worker" in item.name:
                del item
        return True

    def get_resource(self, resource_type):
        """Get a "Worker", "Food" or "Product" from their respective cointainer"""
        __resource = None
        if resource_type == "Worker" and self.road.get_inventory() > 0:
            __resource = Node.road.get_resource()
            self._resources.append(__resource)
            self.node_ui.add_token(__resource.resource_ui)
        elif resource_type == "Food" and self.barn.get_inventory() > 0:
            __resource = Node.barn.get_resource()
            self._resources.append(__resource)
            self.node_ui.add_token(__resource.resource_ui)
        elif resource_type == "Product" and self.magazine.get_inventory() > 0:
            __resource = Node.magazine.get_resource()
            self._resources.append(__resource)
            self.node_ui.add_token(__resource.resource_ui)
        else:
            raise ValueError()   
        
    def return_resource(self, resource_type):

        _resource = self.find_resource(resource_type)

        if "Worker" in _resource.name:
            self.road.insert_resource(_resource)
            self.node_ui.remove_token(_resource.resource_ui)
            return
        elif "Food" in _resource.name:
            self.barn.insert_resource(_resource)
            self.node_ui.remove_token(_resource.resource_ui)
            return
        elif "Product" in _resource.name:
            self.magazine.insert_resource(_resource)
            self.node_ui.remove_token(_resource.resource_ui)
            return
        else:
            raise ValueError()
          
    def find_resource(self, resource_type):
        """Find a local resource by given string."""
        for resource in self._resources:
            if resource_type in resource.name:
                self._resources.remove(resource)
                return resource


class Factory(Node):
    """Factory node, produces a product when a worker is present."""

    __id = 0
    __gui_properties = {"lable":"Factory", "color":"#ff0000", "fill":"#ffffff"}
    def __init__(self):
        """Create the Factory, assign id."""
        super().__init__("Factory" + str(Factory.__id),Factory.__gui_properties)
        Factory.__id += 1
        Node.gui.connect(self.node_ui, Node.magazine.container_ui, {})
    
    def produce(self, worker):
        """Create new produce and stores it locally."""
        self.consume_resources()
        # Don't subtract worker viability in sleep in order to avoid dividing by 0.
        sleep(100/worker.update_viability(0))
        worker.update_viability(-10)
        __produce = Product()
        self._resources.append(__produce)
        self.node_ui.add_token(__produce.resource_ui)

        return

    def random_accident(self, worker):
        """Oh boy here I go killing again."""
        if randint(1,10) <= 2:
            worker.update_viability(-100)

    def update(self):
        """Run an update cycle on the factory."""
        if self.road.get_inventory() > 0:
            self.get_resource("Worker")
            self.produce(self.find_resource("Worker"))
            self.return_resource("Product")
            self.return_resource("Worker")
        else:
           self._time_idle += 1
        

class Field(Node):
    """Field node, produces food when a worker is present."""
    
    __id = 0
    __gui_properties = {"lable":"Field", "color":"#00ff00", "fill":"#ffffff"}
    def __init__(self):
        """Create the Field, assign id."""
        super().__init__("Field" + str(Field.__id), Field.__gui_properties)
        Field.__id += 1
        Node.gui.connect(self.node_ui, Node.barn.container_ui, {})
    
    def produce(self):
        """Create new produce."""
        __produce = Food()
        self._resources.append(__produce)
        self.node_ui.add_token(__produce.resource_ui)
        return

    def random_accident(self, worker):
        """Oh boy here I go killing again."""
        if randint(1,10) <= 2:
            worker.update_viability(-100)

    def update(self):
        """Run an update cycle on the field."""
        if self.road.get_inventory() > 0:
            self.get_resource("Worker")
            self.produce()
            self.return_resource("Food")
            self.return_resource("Worker")
        else:
           self._time_idle += 1
        

class Dining_room(Node):
    """Dining_room node, restores worker viability."""

    __id = 0
    __gui_properties = {"lable":"Dining room", "color":"#555555", "fill":"#ffffff"}

    def __init__(self):
        """Create the Factory, assign id."""
        super().__init__("Dining_room" + str(Dining_room.__id), Dining_room.__gui_properties)
        Dining_room.__id += 1
        Node.gui.connect(Node.barn.container_ui, self.node_ui, {})

    def produce(self, worker):
        """Create new produce."""
        self.consume_resources()
        food_value = randint(10, 40)

        if self.random_accident():
            worker.update_viability(-food_value)
        else:
            worker.update_viability(food_value)
        
    def random_accident(self):
        """Oh boy here I go killing again."""
        if randint(1,5) == 1:
            return True
        else:
             return False

    def update(self):
        """Run an update cycle on the dining room."""
        if self.barn.get_inventory() > 0 and self.road.get_inventory() > 0:
            self.get_resource("Worker")
            self.get_resource("Food")
            self.produce(self.find_resource("Worker"))
            self.return_resource("Worker")
        else:
            self._time_idle += 1
    

class Flat(Node):
    """Flat node, restores worker viability."""

    __id = 0
    __gui_properties = {"lable":"Flat (Lokalen)", "color":"#00c993", "fill":"#ffffff"}

    def __init__(self):
        """Create the Flat, assign id."""
        super().__init__("Flat" + str(Flat.__id), Flat.__gui_properties)
        Flat.__id += 1
        Node.gui.connect(Node.magazine.container_ui, self.node_ui,{})


    def rest(self, worker):
        """Create new produce."""
        self.consume_resources()
        worker.update_viability(randint(10, 40))
    
    def reprocreate(self):
        self.consume_resources()
        self._resources.append(Worker())

    def random_accident(self):
        """Oh boy here I go killing again."""
        if randint(1,5) == 1:
            return True
        else:
             return False

    def update(self):
        """Run an update cycle on the dining room. add reproduce bool to adjust late?"""
        
        if self.magazine.get_inventory() > 0 and self.road.get_inventory() > 0:
            self.get_resource("Worker")
            self.get_resource("Product")
            self.consume_resources()
            if self.road.get_inventory() > 0:
                self.get_resource("Worker")
                self.reprocreate()
                self.return_resource("Worker")
                self.return_resource("Worker")
                self.return_resource("Worker")
            else:
                self.get_resource("Worker")
                self.rest(self.find_resource("Worker"))
                self.return_resource("Worker")
        else:
            self._time_idle += 1
    