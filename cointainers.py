"""Contains the container classes."""
from resource import Worker

class Container():
    """Subclass to Place and super class to the container classes."""
    gui = None
    def __init__(self, name, gui_properties):
        """Initialize the container."""
        self.name = name
        self._resources = []
        self.container_ui = Container.gui.create_place_ui(gui_properties)
    
    def insert_resource(self, resource):
        """Add resource to resources list, won't insert dead workers."""
        if "Worker" in resource.name:
            if resource.update_viability(0) == 0:
                del resource
                return
        self._resources.append(resource)
        self.container_ui.add_token(resource.resource_ui)
        Container.gui.update_ui()
  
    def get_resource(self):
        self.container_ui.remove_token(self._resources[0].resource_ui)
        Container.gui.update_ui()
        return self._resources.pop(0)

    def get_inventory(self):
        return len(self._resources)

class Magazine(Container): 
    """Magazine stores products."""

    def __init__(self):
        """Initialize and sets name."""
        super().__init__("Magazine", {})

class Barn(Container):
    """Barn stores food."""

    def __init__(self):
        """Initialize and sets name."""
        super().__init__("Barn", {})

class Road(Container): 
    """Stores workers while they are moving."""
    
    def __init__(self):
        """Initialize and sets name."""
        super().__init__("Road", {})
    
    def get_resource(self):
        """Reduces worker vialility on the way to work."""
        self.reduce_viabilty(self._resources[0])
        return self._resources.pop(0)


    def reduce_viabilty(self, worker):
        """Traffic hurts the worker and might even kill it."""
        worker.update_viability(-10 * len(self._resources))
        return
            
