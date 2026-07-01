from utils.array import Array
from utils.hashfunc import Hash
from pathlib import Path

class Pipeline:
    def __init__(self):
        print()
        self.hash = Hash()
        self.array = Array()
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.data_dir / "hash-info.txt"
        self.data_file.touch()
        self.hash_managment()


    def hash_managment(self):
       # persistent hash counting
        with self.data_file.open("r") as file:
            if file.read() == "":
                self.hash_count = 0
                self.array_init(16)
            else:
                with self.data_file.open("r") as file:
                    line_count = file.readlines()

                for i in range(len(line_count)):
                    if line_count[i].startswith("hash-size:"):
                        self.hash_count = line_count[i].replace("hash-size:", "", 1).strip()
                        self.hash_count = int(self.hash_count)
                
                self.array_init(self.hash_count*2)

            # re=hashing
                with self.data_file.open("r") as file:
                            line_count = file.readlines()

                for i in range(len(line_count)):
                    if line_count[i].startswith("k:"):
                        self.key = line_count[i].replace("k:", "", 1).strip()
                        self.key = str(self.key)
                        if i+1 < len(line_count) and line_count[i+1].startswith("v:"):
                            self.value = line_count[i+1].replace("v:", "", 1).strip()
                            self.value = str(self.value)
                        self.hashed_key = self.hash.hasher(self.key)
                        self.store_hash(self.key, self.value)

    def array_init(self, ARRAY_SIZE):
        self.ARRAY_SIZE = ARRAY_SIZE
        self.array_update = self.ARRAY_SIZE
        self.array = Array().array_create(self.ARRAY_SIZE)

        
    def value_input(self, key, value):
        self.key = key
        self.value = value
        self.hashed_key = self.hash.hasher(self.key)
        
        failsafe = self.store_hash(self.key, self.value)

        if failsafe is True:
            self.store_data(self.key, self.value)
            return_value = "hash successful"
            return(return_value)
        
        elif failsafe is False:
            return_value = "hash map is full"
            return(return_value)
        elif failsafe == "invalid":
            return_value = "key not allowed"
            return(return_value)
        else:
            return_value = "unexpected hash error occured"
            return(return_value)
    
    def store_data(self, key, value):
        
        self.key = key
        self.value = value 

        self.data_file.touch()

        with self.data_file.open("a") as file:
            if self.hash_count == 0:
                self.hash_count += 1
                file.write(f"hash-size: {self.hash_count}\n")
            else:
                self.hash_count += 1

            file.write("----------------------\n")
            file.write(f"k: {self.key}\n")
            file.write(f"v: {self.value}\n")
            
        with self.data_file.open("r") as file:
            line_count = file.readlines()

        for i in range(len(line_count)):
            if line_count[i].startswith("hash-size:"):
                line_count[i] = f"hash-size: {self.hash_count}\n"

        with self.data_file.open("w") as file:
            file.writelines(line_count)
        
        self.map_congestion = self.hash_count/self.ARRAY_SIZE

        if self.map_congestion >= 0.75:
            self.hash_managment()


    def store_hash(self, key, value):
        self.key = key
        self.value = value 
        Array_index = self.hashed_key % self.ARRAY_SIZE
        start_index = Array_index
        while True:
            if self.array[Array_index][0] == self.key:
                return_value = "invalid"
                return(return_value)
            
            if self.array[Array_index][0] == 0:
                self.array[Array_index][0] = self.key
                self.array[Array_index][1] = self.value
                return_value = True
                return(return_value)
            else: 
                Array_index = (Array_index + 1) % self.ARRAY_SIZE
                if start_index == Array_index:
                    return_value = False
                    return(return_value)

    def retrieve_key(self, key):
        self.key = key
        self.retrieval_hash = self.hash.hasher(self.key)
        self.retrieval_index = self.retrieval_hash % self.ARRAY_SIZE
        start_index = self.retrieval_index

        while True:
            self.key_validate = self.array[self.retrieval_index][0]
            if self.key == self.key_validate:
                return_value = f"{self.array[self.retrieval_index][0]}, {self.array[self.retrieval_index][1]}"
                return(return_value)
            elif self.key_validate == 0:
                return_value = "key does not exist"
                return(return_value)
            else:
                self.retrieval_index = (self.retrieval_index + 1) % self.ARRAY_SIZE
                if start_index == self.retrieval_index:
                    return_value = "hash table is full"
                    return(return_value)
                     

