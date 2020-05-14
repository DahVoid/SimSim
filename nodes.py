"""Cointains the classes responsible for producing resources."""
# Todo look at dining room rest or reprocreate
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
                self.node_ui.remove_token(item.resource_ui)
                Node.gui.remove(item.resource_ui)
                self._resources.remove(item)
                del item
                Node.gui.update_ui()
                
    def get_resource(self, resource_type):
        """Get a "Worker", "Food" or "Product" from their respective cointainer"""
        __resource = None
        if resource_type == "Worker" and self.road.get_inventory() > 0:
            __resource = Node.road.get_resource()
            self._resources.append(__resource)
            self.node_ui.add_token(__resource.resource_ui)
            Node.gui.update_ui()
        elif resource_type == "Food" and self.barn.get_inventory() > 0:
            __resource = Node.barn.get_resource()
            self._resources.append(__resource)
            self.node_ui.add_token(__resource.resource_ui)
            Node.gui.update_ui()
        elif resource_type == "Product" and self.magazine.get_inventory() > 0:
            __resource = Node.magazine.get_resource()
            self._resources.append(__resource)
            self.node_ui.add_token(__resource.resource_ui)
            Node.gui.update_ui()
        else:
            raise ValueError()   
        
    def return_resource(self, resource_type):

        _resource = self.find_resource(resource_type)

        if "Worker" in _resource.name:
            self.road.insert_resource(_resource)
            self.node_ui.remove_token(_resource.resource_ui)
            Node.gui.update_ui()
            
        elif "Food" in _resource.name:
            self.barn.insert_resource(_resource)
            self.node_ui.remove_token(_resource.resource_ui)
            Node.gui.update_ui()
            
        elif "Product" in _resource.name:
            self.magazine.insert_resource(_resource)
            self.node_ui.remove_token(_resource.resource_ui)
            Node.gui.update_ui()
            
        else:
            raise ValueError()
          
    def find_resource(self, resource_type):
        """Find a local resource by given string."""
        #todo  fix this so we dont have to return the worker
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
        # Don't subtract worker viability in sleep in order to avoid dividing by 0.
        # sleep(1 + 20/worker.update_viability(0))
        worker.update_viability(-10)
        __produce = Product()
        self._resources.append(__produce)
        self.node_ui.add_token(__produce.resource_ui)
        Node.gui.update_ui()
        # Put back woker in inventory
        self._resources.append(worker)

    def random_accident(self, worker):
        """Oh boy here I go killing again."""
        if randint(1,10) <= 2:
            worker.update_viability(-100)
 
    def update(self):
        """Run an update cycle on the factory."""
        if self.road.get_inventory() > 0:
            self.get_resource("Worker")
            __worker = self.find_resource("Worker")
            # Put back woker in inventory
            self._resources.append(__worker)
            self.random_accident(__worker)
            if __worker.update_viability(0) < 1:
                self.return_resource("Worker")
                return
            else:
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
    
    def random_accident(self, worker):
        """Oh boy here I go killing again."""
        if randint(1,10) <= 2:
            worker.update_viability(-100)

    def produce(self, worker):
        """Create new produce."""
        __produce = Food()
        self._resources.append(__produce)
        self.node_ui.add_token(__produce.resource_ui)
        Node.gui.update_ui()
        self.random_accident(worker)
        # Put back worker to inventory
        self._resources.append(worker)

    def update(self):
        """Run an update cycle on the field."""
        if self.road.get_inventory() > 0:
            self.get_resource("Worker")
            self.produce(self.find_resource("Worker"))
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
        
        # Put back worker to inventory
        self._resources.append(worker)
        
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
    __gui_properties = {"lable":"Lokalen™", "color":"#00c993", "fill":"#000000"}

    def __init__(self):
        """Create the Flat, assign id."""
        super().__init__("Flat" + str(Flat.__id), Flat.__gui_properties)
        Flat.__id += 1
        Node.gui.connect(Node.magazine.container_ui, self.node_ui,{})

    def rest(self, worker):
        """Create new produce."""
        self.consume_resources()
        worker.update_viability(randint(10, 60))
        # Put back worker to inventory
        self._resources.append(worker)
    
    def reprocreate(self):
        __child = Worker()
        self._resources.append(__child)
        self.node_ui.add_token(__child.resource_ui)
        Node.gui.update_ui()

    def update(self):
        """Run an update cycle on the dining room. add reproduce bool to adjust late?"""
        
        if self.magazine.get_inventory() > 0 :
            self.get_resource("Worker")
            self.get_resource("Product")
            if self.road.get_inventory() > 0  and self.road.get_inventory() < 10 :
                self.get_resource("Worker")
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
            self._time_idle += 1
    