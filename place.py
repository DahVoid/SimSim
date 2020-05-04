"""Module cointaining the place class, the super class for all visitable places. Todo: delete connections between places."""
class Place:
    """Super class to all the visitable places."""

    def __init__(self, name):
        """Initialze the object."""
        self._name = name
        self._resources = []
        self._ingoing_connections = []
        self._outgoing_connections = []
    
    def connect_place(self, place):
        """Create a connection from self to another place."""
        self.connect_outgoing(place)
        place.connect_ingoing(self)
        # Debatable if return is needed.
        if place in self._outgoing_connections and self in place._ingoing_connections:
           return True
        else:
            return False

    def connect_ingoing(self, place):
        """Create an ingoing connection from place to self."""
        self._ingoing_connections.append(place)

    def connect_outgoing(self, place):
        """Crearte an outgoing connection from self to place."""
        self._outgoing_connections.append(place)
    
        