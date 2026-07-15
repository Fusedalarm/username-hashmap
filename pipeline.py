from hash import Hash, Array
from linkedlist import LinkedList
from pathlib import Path
import hashlib
from cryptography.fernet import Fernet


class Pipeline:
    def __init__(self):
        #create dir and files required
        self.initverif = False
        array = Array()
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
       
        self.data_file = self.data_dir / "hash-info.txt"
        self.data_file.touch()

        self.token = "amongusman"
        self.token_hashed = hashlib.sha256(self.token.encode()).digest()
        # persistent hash counting
        with self.data_file.open("r") as file:
            if file.read() == "":
                self.hash_count = 0
                self.array_size = 16 #default
            else:
                with self.data_file.open("r") as file:
                    line_count = file.readlines()
                    # add decrypting here

                for i in range(len(line_count)):
                    if line_count[i].startswith("hash-size:"):
                        self.hash_count = line_count[i].replace("hash-size:", "", 1).strip()
                        self.hash_count = int(self.hash_count)
                        self.array_size = self.hash_count*2
                
            self.hash_map = array.create(self.array_size)
        
        # re-hashing
        with self.data_file.open("r") as file:
                    line_count = file.readlines()
                    # add decrypting here

        for i in range(len(line_count)):
            if line_count[i].startswith("k:"):
                self.key = line_count[i].replace("k:", "", 1).strip()
                self.key = str(self.key)
                
                # re hash
                if i+1 < len(line_count) and line_count[i+1].startswith("v:"):
                    self.value = line_count[i+1].replace("v:", "", 1).strip()
                    self.value = str(self.value)
                self.hashed_key = Hash().value(self.key) % self.array_size
                
                if self.hash_map[self.hashed_key][0] == 0:
                    linkedlist = LinkedList()
                    self.hash_map[self.hashed_key][0] = linkedlist
                    a = linkedlist.append(self.key, self.value)
                else:
                    a = self.hash_map[self.hashed_key][0].append(self.key, self.value) # append to exsisting
        
            # delete
            if line_count[i].startswith("Delete:"):
                self.key = line_count[i].replace("Delete:", "", 1).strip()
                self.key = str(self.key)
                
                raw_hash = Hash().value(self.key)
                binned_hash = raw_hash % self.array_size

                if self.hash_map[binned_hash][0] == 0:
                    break
                
                self.retrieved_pair = self.hash_map[binned_hash][0].delete(self.key)
        
        self.initverif = True
 

    def hash_value(self, key, value):
        self.key = key
        self.value = value
        
        raw_hash = Hash().value(self.key)
        binned_hash = raw_hash % self.array_size
        
        # store the key-value
        if self.hash_map[binned_hash][0] == 0:
            linkedlist = LinkedList()
            self.hash_map[binned_hash][0] = linkedlist
            a = linkedlist.append(self.key, self.value)
        else:
            a = self.hash_map[binned_hash][0].append(self.key, self.value) # append to exsisting
        
        if a == False: # make sure that hash functions is valid
            return False
        else:    
            return True

    def retrieve(self, key):

        raw_hash = Hash().value(key)
        binned_hash = raw_hash % self.array_size

        if self.hash_map[binned_hash][0] == 0:
            return False
        
        retrieved_pair = self.hash_map[binned_hash][0].retrieve(key)
        if retrieved_pair == False:
            return False
        else:
            return retrieved_pair.key, retrieved_pair.value

    def delete(self, key):

        raw_hash = Hash().value(key)
        binned_hash = raw_hash % self.array_size

        if self.hash_map[binned_hash][0] == 0:
            return False
        
        retrieved_pair = self.hash_map[binned_hash][0].delete(key)
        if retrieved_pair == False:
            return False
        else:
            self.store_delete(key)
            return True

    def store_hash(self, key, value):
        
        raw_hash = Hash().value(key)
        self.data_file.touch()

        with self.data_file.open("a") as file:
            if self.hash_count == 0:
                self.hash_count += 1
                file.write(f"hash-size: {self.hash_count}\n")
            else:
                self.hash_count += 1

            file.write("----------------------\n")
            file.write(f"k:{key}\n")
            file.write(f"v:{value}\n")
            file.write(f"h:{raw_hash}\n")
        
        with self.data_file.open("r") as file:
            line_count = file.readlines()

        for i in range(len(line_count)):
            if line_count[i].startswith("hash-size:"):
                line_count[i] = f"hash-size: {self.hash_count}\n"

        with self.data_file.open("w") as file:
            file.writelines(line_count)

    def store_delete(self, key):
        self.data_file.touch()

        with self.data_file.open("a") as file:
            if self.hash_count == 0:
                self.hash_count += 1
                file.write(f"hash-size: {self.hash_count}\n")
            else:
                self.hash_count += 1

            file.write("----------------------\n")
            file.write(f"Delete:{key}\n")
            
