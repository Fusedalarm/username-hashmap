import hashlib

class Hash:
    def __init__(self):
        ...
        
    def value(self, input_value):
        self.input_value = input_value 
        if self.input_value == "":
            print("no value detected")
            return False
        try:
            hashed_value = hashlib.sha256(self.input_value.encode()).digest()
            hashed_value = int.from_bytes(hashed_value, "big") #big reads bytes right to left little is vice versa
         
            return hashed_value
        
        except TypeError:
            print("unsupported input")
            return None
        

class Array:
    @staticmethod
    def create(array_size):
        #will lose an array once it has been created when resizing eg
        outer_list = []

        for i in range(array_size):
            inner_list = []
            for j in range(1):
                inner_list.append(0) #initial number 0
            outer_list.append(inner_list)
        
        return outer_list