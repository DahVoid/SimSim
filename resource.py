"""Contain all resources."""

class Resource:
    """Base class for resources, handles ui and name."""

    gui = None
    def __init__(self, name, gui_properties):
        """Set resource name and ui."""
        self.name = name
        self.resource_ui = self.gui.create_token_ui(gui_properties)
    
    def to_dict(self):
        """Return a dict with resource name."""
        resource_dict = {
            "name": self.name,
            }
        return resource_dict

    @staticmethod
    def create_from_dict(res_dict):
        """Create resource based upon name in res_dict."""
        res_name = res_dict["name"]

        if "Product" in res_name:
            res = Product()
        elif "Food" in res_name:
            res = Food()
        elif "Worker" in res_name:
            res = Worker()
            res.update_viability(100 - res_dict["viability"])
        
        return res

class Worker(Resource):
    """Handle id, gui_properties and worker viability."""

    _id = 0
    _gui_properties = {"color":"#888888"}
    def __init__(self):
        """Create worker, sets viability."""
        super().__init__("Worker" + str(Worker._id), Worker._gui_properties)
        Worker._id += 1
        self._viability = 100
    
    def update_viability(self, value):
        """Change the viability by the parameter. Return the current viability."""
        self._viability += value
        
        if self._viability > 100:
            self._viability = 100
        elif self._viability < 0:
            self._viability = 0

        return self._viability

    def to_dict(self):
        """Return a dict with resource name and viability."""
        resource_dict = {
            "name": self.name,
            "viability": self.update_viability(0)
            }
        return resource_dict

class Food(Resource):
    """Handle id, gui_properties."""

    _id = 0
    _gui_properties = {"color":"#00ff00"}
    def __init__(self):
        """Create food."""
        super().__init__("Food" + str(Food._id), Food._gui_properties)
        Food._id += 1

class Product(Resource):
    """Handle id, gui_properties."""

    _id = 0
    _gui_properties = {"color":"#dddd77"}
    def __init__(self):
        """Create Product."""
        super().__init__("Product" + str(Product._id), Product._gui_properties)
        Product._id += 1

