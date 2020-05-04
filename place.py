

class place:
"""Super class to all the visitable places."""
    def __init__(self, name):
        self._name = name
        self._resources = ()
        self._ingoing_connections = ()
        self._outgoing_connections = ()
    
    def connect_place(Place):
        self.connect_outgoing(Place)
        Place.connect_ingoing(Self)
        # Debatable if return is needed.
       if place in self._outgoing_connections and self in place._ingoing_connections:
           return True
        else:
            return False
    
    def connect_ingoing(Place):
        self._ingoing_connections.add(Place)
        
    def connect_outgoing(Place):
        self._outgoing_connections.add(Place)
    
        