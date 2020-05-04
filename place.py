"""Module cointaining the place class, the super class for all visitable places. Todo: delete connections between places."""
class place:
    """Super class to all the visitable places."""

    def __init__(self, name):
        """Initialze the object."""
        self._name = name
        self._resources = []
        self._ingoing_connections = []
        self._outgoing_connections = []
    
    def connect_place(self, Place):
        """Create a connection from self to another Place."""
        self.connect_outgoing(Place)
        Place.connect_ingoing(self)
        # Debatable if return is needed.
        if Place in self._outgoing_connections and self in Place._ingoing_connections:
           return True
        else:
            return False

    def connect_ingoing(self, Place):
        """Create an ingoing connection from Place to self."""
        self._ingoing_connections.append(Place)

    def connect_outgoing(self, Place):
        """Crearte an outgoing connection from self to place."""
        self._outgoing_connections.append(Place)
    
        