"""Cointains the classes responsible for producing resources."""
from resource import Food, Product, Worker
from time import sleep
from random import randint


class Node():
    """Superclass for producing classes."""

    barn = None
    road = None
    magazine = None

    def __init__(self, name):
        """Initialize the Node."""
        self.name = name
        self._resources = []
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
        for item in self._resources:
            if not "Worker" in item.name:
                del item
        return True

    def get_resource(self, resource_type):
        """Get a "Worker", "Food" or "Product" from their respective cointainer"""

        if resource_type == "Worker" and self.road.get_inventory() > 0:
            self._resources.append(Node.road.get_resource())

        elif resource_type == "Food" and self.barn.get_inventory() > 0:
            self._resources.append(Node.barn.get_resource())

        elif resource_type == "Product" and self.magazine.get_inventory() > 0:
            self._resources.append(Node.magazine.get_resource())
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
            self.produce(self.find_resource("Worker"))
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
        self._resources.append(Food())
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
            self.barn.insert_resource(self.find_resource("Food"))
            self.road.insert_resource(self.find_resource("Worker"))
        else:
           self._time_idle += 1
        

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
        """Run an update cycle on the dining room."""
        if self.barn.get_inventory() > 0 and self.road.get_inventory() > 0:
            self.get_resource("Worker")
            self.get_resource("Food")
            self.produce(self.find_resource("Worker"))
            self.road.insert_resource(self.find_resource("Worker"))
        else:
            self._time_idle += 1
    

class Flat(Node):
    """Flat node, restores worker viability."""

    __id = 0

    def __init__(self):
        """Create the Flat, assign id."""
        super().__init__("Flat" + str(Flat.__id))
        Flat.__id += 1

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
            if self.road.get_inventory() > 0:
                self.get_resource("Worker")
                self.reprocreate()
                self.road.insert_resource(self.find_resource("Worker"))
                self.road.insert_resource(self.find_resource("Worker"))
                self.road.insert_resource(self.find_resource("Worker"))
            else:
                self.get_resource("Worker")
                self.rest(self.find_resource("Worker"))
                self.road.insert_resource(self.find_resource("Worker"))
        else:
            self._time_idle += 1
    