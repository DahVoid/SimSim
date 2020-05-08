"""Cointains the classes responsible for producing resources."""
from place import Place
from resource import Food, Product, Worker
from time import sleep
from random import randint


class Node(Place):
    """Superclass for producing classes."""

    barn = None
    road = None
    magazine = None

    def __init__(self, name):
        """Initialize the Node."""
        super().__init__(name)
        self._time_idle = 0
    
    def update(self):
        """Update the state of the node."""
        raise NotImplementedError
    
    def produce(self):
        """Produce product."""
        raise NotImplementedError

    def consume_resources(self):
        """Consume the resources."""
        # We trust that our get_resource bring the correct ones.
        for resource in self._resources:
            if not "Worker" in resource.name:
                del resource
        return True

    def get_resource(self, resource_type):
        """Get a "Worker", "Food" or "Product" from their respective cointainer"""

        if resource_type == "Worker" and self.road.get_inventory() > 0:
            self._resources.append(Node.road.get_resource)
            return True
        elif resource_type == "Food" and self.barn.get_inventory() > 0:
            self._resources.append(Node.road.get_resource)
            return True
        elif resource_type == "Product" and self.magazine.get_inventory() > 0:
            self._resources.append(Node.road.get_resource)
            return True
        else:
            return False

    def find_resource(self, resource_type):
        """Find a local resource by given string."""
        for resource in self._resources:
            if resource_type in resource.name:
                return self._resource.pop(self._resources.index(resource))

class Factory(Node):
    """Factory node, produces a product when a worker is present."""

    __id = 0

    def __init__(self):
        """Create the Factory, assign id."""
        super().__init__("Factory" + str(Factory.__id))
        Factory.__id += 1
  
    def produce(self, worker):
        """Create new produce and stores it locally."""
        self.consume_resources()
        # Don't subtract worker viability in sleep in order to avoid dividing by 0.
        sleep(100/worker.update_viability(0))
        worker.update_viability(-10)
        self._resources.append(Product())
        return

    def random_accident(self, worker):
        """Oh boy here I go killing again."""
        if randint(1,10) <= 2:
            worker.update_viability(-100)

    def update(self):
        """Run an update cycle on the factory."""
        # get resources
        if self.road.get_inventory() > 0:
            self.get_resource("Worker")
            self.produce(self.find_resource(Worker))
            self.magazine.insert_resource(self.find_resource("Product"))
            self.road.insert_resource(self.find_resource("Worker"))
        else:
           self._time_idle += 1
        

class Field(Node):
    """Field node, produces food when a worker is present."""
    
    __id = 0

    def __init__(self):
        """Create the Field, assign id."""
        super().__init__("Field" + str(Field.__id))
        Field.__id += 1
        self
    
    def produce(self):
        """Create new produce."""
        self.consume_resources()
        self._resources.append(Food())
        return

    def random_accident(self, worker):
        """Oh boy here I go killing again."""
        if randint(1,10) <= 2:
            worker.update_viability(-100)

    def update(self):
        """Run an update cycle on the field."""
        # get resources
        if self.get_resource("Worker"):

        else:
            pass
        
        # use resources


        # return 
            pass

class Dining_room(Node):
    """Dining_room node, restores worker viability."""

    __id = 0

    def __init__(self):
        """Create the Factory, assign id."""
        super().__init__("Dining_room" + str(Dining_room.__id))
        Dining_room.__id += 1

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
        """Run an update cycle on the factory."""
        # get resources
        if self.get_resource("Worker"):

        
        # use resources


        # return 
            pass

class Flat(Node):
    """Flat node, restores worker viability."""

    __id = 0

    def __init__(self):
        """Create the Flat, assign id."""
        super().__init__("Flat" + str(Flat.__id))
        Flat.__id += 1

    def produce(self, worker):
        """Create new produce."""
        self.consume_resources()
        raise NotImplementedError
        
    def random_accident(self):
        """Oh boy here I go killing again."""
        if randint(1,5) == 1:
            return True
        else:
             return False

    def update(self):
        # get resources
        if self.get_resource("Worker"):

        
        # use resources


        # return 
            pass
