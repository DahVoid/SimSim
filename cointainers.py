"""Contains the container classes."""
from place import Place

class Container(Place):
    """Subclass to Place and super class to the container classes."""

    def __init__(self, name):
        """Initialize the container."""
        super().__init__(name)
    
    def virtual_insert(self, resource):
        """Add resource to resources list."""
        self._resources.append(resource)

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
    