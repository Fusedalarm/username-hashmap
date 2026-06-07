#hashing function

class Hash:
    def __init__(self):
        ...

    def hasher(self, input_value):
        self.input_value = input_value 
        if self.input_value == "":
            print("no value detected")
            return None
        try:
            hashed_value = hash(self.input_value)
            return hashed_value
        except TypeError:
            print("unsupported input")
            return None
        
       

        
       

    
    
