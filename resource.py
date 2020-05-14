class Resource:
    gui = None
    def __init__(self, name, gui_properties):
        self.name = name
        self.resource_ui = self.gui.create_token_ui(gui_properties)

class Worker(Resource):
    __id = 0
    __gui_properties = {"color":"#000000"}
    def __init__(self):
        super().__init__("Worker" + str(Worker.__id), Worker.__gui_properties)
        Worker.__id += 1
        self.viability = 100 # gör privat
    
    def update_viability(self, value):
        """Change the viability by the parameter. Return the current viability."""
        self.viability + value
        
        if self.viability > 100:
            self.viability = 100
        elif self.viability < 0:
            self.viability = 0

        return self.viability

class Food(Resource):
    __id = 0
    __gui_properties = {"color":"#00ff00"}
    def __init__(self):
        super().__init__("Food" + str(Food.__id), Food.__gui_properties)
        Food.__id += 1

class Product(Resource):
    __id = 0
    __gui_properties = {"color":"#dddd77"}
    def __init__(self):
        super().__init__("Product" + str(Product.__id), Product.__gui_properties)
        Product.__id += 1

