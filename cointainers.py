"""Contains the container classes."""
from resource import Worker, Food, Product
from threading import Lock

class Container():
    """Subclass to Place and super class to the container classes."""
    
    gui = None
    def __init__(self, name, gui_properties):
        """Initialize the container."""
        self.lock = Lock()
        self.name = name
        self._resources = []
        self.container_ui = Container.gui.create_place_ui(gui_properties)
    
    def insert_resource(self, resource):
        """Add resource to resources list, won't insert dead workers."""
        self.lock.acquire()
        try:
            if "Worker" in resource.name:
                if resource.update_viability(0) <= 0:
                    Container.gui.remove(resource.resource_ui)
                    del resource
                    Container.gui.update_ui()
                    return
            self._resources.append(resource)
            self.container_ui.add_token(resource.resource_ui)
            Container.gui.update_ui()
        finally:
            self.lock.release()
  
    def get_resource(self):
        """Return a poped local resource."""
        self.lock.acquire()
        try:
            if len(self._resources) > 0:
                self.container_ui.remove_token(self._resources[0].resource_ui)
                Container.gui.update_ui()
                return self._resources.pop(0)
            else:
                return None
        finally:
            self.lock.release()

    def get_inventory(self):
        """Return the amount of locally stored resources."""
        self.lock.acquire()
        try:
            return len(self._resources)
        finally:
            self.lock.release()      

    def to_dict(self):
        """Return a dictionary with container name and resources."""
        res_list = []
        for res in self._resources:
            res_list.append(res.to_dict())

        cont_dict = {
        "name": self.name,
        "resources": res_list
            }
        return cont_dict

    @staticmethod
    def create_from_dict(cont_dict):
        """Return a container based upon parameter dict."""
        cont_name = cont_dict["name"]
        cont = None
        if "Magazine" in cont_name:
            cont = Magazine()
        elif "Barn" in cont_name:
            cont = Barn()
        elif "Road" in cont_name:
            cont = Road()

        for res_dict in cont_dict["resources"]:
            res_name = res_dict["name"]
            res = None
            if "Food" in res_name:
                res = Food.create_from_dict(res_dict)
                cont._resources.append(res)
                cont.container_ui.add_token(res.resource_ui)
            elif "Product" in res_name:
                res = Product.create_from_dict(res_dict)
                cont._resources.append(res)
                cont.container_ui.add_token(res.resource_ui)
            elif "Worker" in res_name:
                res = Worker.create_from_dict(res_dict)
                cont._resources.append(res)
                cont.container_ui.add_token(res.resource_ui)

            Container.gui.update_ui()

        return cont

class Magazine(Container): 
    """Magazine stores products."""
    
    def __init__(self):
        """Initialize and sets name."""
        self.__gui_properties = {"lable":"Dônkkällare","color":"#ff0000", "fill":"#000000"}
        super().__init__("Magazine", self.__gui_properties)

class Barn(Container):
    """Barn stores food."""
   
    def __init__(self):
        """Initialize and sets name."""
        self.__gui_properties = {"lable":"Barn","color":"#00ff00", "fill":"#ffffff"}
        super().__init__("Barn", self.__gui_properties)

class Road(Container): 
    """Stores workers while they are moving."""

    def __init__(self):
        """Initialize and sets name."""
        self.__gui_properties = {"lable":"Road","color":"#000000", "fill":"#ffffff"}
        super().__init__("Road", self.__gui_properties)
    
    def get_resource(self):
        """Reduces worker vialility on the way to work."""
        self.lock.acquire()
        try:
            if len(self._resources) > 0:
                worker = self._resources.pop(0)
                self.__reduce_viabilty(worker)
                self.container_ui.remove_token(worker.resource_ui)
                Container.gui.update_ui()
                return worker
            else:
                return None
        finally:
            self.lock.release()

    def __reduce_viabilty(self, worker):
        """Traffic hurts the worker and might even kill it."""
        worker.update_viability(-3 * len(self._resources))
        return
            
