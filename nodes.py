"""Cointains the classes responsible for producing resources."""
from place import Place

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

    def reduce_viability(self, worker):
        """Why hurt the worker? :(."""
        pass
    
    def produce(self):
        """Create new produce."""
        self.use_resources()
        pass

    def random_accident(self, worker):
        """Oh boy here I go killing again."""
        pass

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
        pass

    def random_accident(self, worker):
        """Oh boy here I go killing again."""
        pass

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

    def reduce_viability(self, worker):
        """Why hurt the worker? :(."""
        pass
    
    def produce(self):
        """Create new produce."""
        self.use_resources()
        pass

    def random_accident(self, worker):
        """Oh boy here I go killing again."""
        pass

    def update(self):
        """Run an update cycle on the factory."""
        pass
