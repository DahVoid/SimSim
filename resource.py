class resource:
    def __init__(self, name):
        self.name = name

class worker(resource):
    __id = 0
    def __init__(self):
        super.__init__("Worker" + str(worker.__id))
        worker.__id += 1
        self.viability = 100
    
    def update_viability(self, value):
        """Change the viability by the parameter. Return the current viability"""
        self.viability + value
        
        if self.viability > 100:
            self.viability = 100
        elif self.viability < 0:
            self.viability = 0

        return self.viability

class food(resource):
    __id = 0
    def __init__(self):
        super.__init__("Food" + str(food.__id))
        food.__id += 1


class product(resource):
    __id = 0
    def __init__(self):
        super.__init__("Product" + str(product.__id))
        product.__id += 1

