#hashing function

class hash:
    def __init__(self, input_value):
        self.input_value = input_value 
        
    def hasher(self):
        if input_value == "":
            print("no value detected")
            return None

        hashed_value = hash(input_value)
        return hashed_value