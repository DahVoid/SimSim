"""Contains the container classes."""
from place import Place

class Container(Place):
    """Subclass to Place and super class to the container classes."""

    def __init__(self, name):
        """Initialize the container."""
        super().__init__(name)
    
    def insert_resource(self, resource):
        """Add resource to resources list, won't insert dead workers."""
        if "Worker" in resource.name:
            if resource.update_viability == 0:
                del resource

        self._resources.append(resource)
    
    def get_resource(self):
        return self._resources.pop(0)

    def get_inventory(self):
        return len(self._resources)

class Magazine(Container): 
    """Magazine stores products."""

    def __init__(self):
        """Initialize and sets name."""
        super().__init__("Magazine")

class Barn(Container):
    """Barn stores food."""

    def __init__(self):
        """Initialize and sets name."""
        super().__init__("Barn")

class Road(Container): 
    """Stores workers while they are moving."""
    
    def __init__(self):
        """Initialize and sets name."""
        super().__init__("Road")
    
    def get_resource(self):
        """Reduces worker vialility on the way to work."""
        self.reduce_viabilty(self._resources[0])
        return self._resources.pop(0)


    def reduce_viabilty(self, worker):
        """Traffic hurts the worker and might even kill it."""
        if worker.update_viability(-10 * len(self._resources)) == 0:
            del worker
        else:
            return
            
