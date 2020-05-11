class resource:
    def __init__(self, name):
        self.name = name

class Worker(resource):
    __id = 0
    def __init__(self):
        super().__init__("Worker" + str(Worker.__id))
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

class Food(resource):
    __id = 0
    def __init__(self):
        super.__init__("Food" + str(Food.__id))
        Food.__id += 1

class Product(resource):
    __id = 0
    def __init__(self):
        super.__init__("Product" + str(Product.__id))
        Product.__id += 1

