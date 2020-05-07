"""Cointains the classes responsible for producing resources."""
from place import Place
from resource import Food, Product, Worker
from time import sleep
from random import randint
class Node(Place):
    """Superclass for producing classes."""

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

    def use_resources(self):
        """#Consume the resources."""
        # We trust that our get_resource bring the correct ones.
        for resource in self._resources:
            if not "Worker" in resource.name:
                del resource
        return True

    def _check_demand(self):
        pass

    def _lower_supply(self):
        pass
    
    def _increase_supply(self):
        pass

class Factory(Node):
    """Factory node, produces a product when a worker is present."""

    __id = 0

    def __init__(self):
        """Create the Factory, assign id."""
        super().__init__("Factory" + str(Factory.__id))
        Factory.__id += 1

    def produce(self, worker):
        """Create new produce and stores it locally."""
        self.use_resources()
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
        pass

class Field(Node):
    """Field node, produces food when a worker is present."""
    
    __id = 0

    def __init__(self):
        """Create the Field, assign id."""
        super().__init__("Field" + str(Field.__id))
        Field.__id += 1
    
    def produce(self):
        """Create new produce."""
        self.use_resources()
        self._resources.append(Food())
        return

    def random_accident(self, worker):
        """Oh boy here I go killing again."""
        if randint(1,10) <= 2:
            worker.update_viability(-100)

    def update(self):
        """Run an update cycle on the factory."""
        pass

class DiningRoom(Node):
    """DiningRoom node, restores worker viability."""

    __id = 0

    def __init__(self):
        """Create the Factory, assign id."""
        super().__init__("Factory" + str(Factory.__id))
        Factory.__id += 1

    def produce(self, worker):
        """Create new produce."""
        self.use_resources()
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
        pass
