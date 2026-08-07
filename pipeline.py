from hash import Hash, Array
from linkedlist import LinkedList
from pathlib import Path
import hashlib
from fernet import Encrypt


class Pipeline:
    def __init__(self, password):
        #create dir and files required
        self.initverif = True
        self.encrypt = Encrypt(password)
        self.linkedlist = LinkedList()
        array = Array()
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
       
        self.data_file = self.data_dir / "hash-info.bin"
        self.data_file.touch()

        self.collisions = self.linkedlist.collision_count 

        # persistent hash counting
        with self.data_file.open("rb") as file:
            if file.read() == b"":
                self.hash_count = 0
                self.array_size = 16 #default
            else:
                with self.data_file.open("rb") as file:
                    raw_lines = file.readlines()
                
                line_count = []
                for line in raw_lines:
                    decrypted = self.encrypt.decode(line)
                    if decrypted != False:
                        line_count.append(decrypted)
                    else:
                        self.initverif = False
                        return
                        
                for i in range(len(line_count)):
                    if line_count[i].startswith("hash-size:"):
                        self.hash_count = line_count[i].replace("hash-size:", "", 1).strip()
                        self.hash_count = int((self.hash_count))
                        self.array_size = self.hash_count*2
                
            self.hash_map = array.create(self.array_size)
        
        # re-hashing
        with self.data_file.open("rb") as file:
            raw_lines = file.readlines()
                    
        # decrypt
        line_count = []
        for line in raw_lines:
            decrypted = self.encrypt.decode(line)
            if decrypted != False:
                line_count.append(decrypted)
            else: 
                self.initverif = False
                return 

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
                    self.hash_map[self.hashed_key][0] = self.linkedlist
                    a = self.linkedlist.append(self.key, self.value)
                else:
                    a = self.hash_map[self.hashed_key][0].append(self.key, self.value) # append to exsisting
                self.collisions = self.linkedlist.collision_count # collisions count updating

            # delete
            if line_count[i].startswith("Delete:"):
                self.key = line_count[i].replace("Delete:", "", 1).strip()
                self.key = str(self.key)
                
                raw_hash = Hash().value(self.key)
                binned_hash = raw_hash % self.array_size

                if self.hash_map[binned_hash][0] != 0:
                    self.retrieved_pair = self.hash_map[binned_hash][0].delete(self.key)

    def hash_value(self, key, value):
        self.key = key
        self.value = value
        
        raw_hash = Hash().value(self.key)
        binned_hash = raw_hash % self.array_size
        
        # store the key-value
        if self.hash_map[binned_hash][0] == 0:
            self.hash_map[binned_hash][0] = self.linkedlist
            a = self.linkedlist.append(self.key, self.value)
        else:
            a = self.hash_map[binned_hash][0].append(self.key, self.value) # append to exsisting
        
        if a == False: # make sure that hash functions is valid
            return False
        else:   
            self.collisions = self.linkedlist.collision_count 
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

        with self.data_file.open("ab") as file:
            if self.hash_count == 0:
                self.hash_count += 1
                file.write(self.encrypt.encoder(f"hash-size: {self.hash_count}"))
            else:
                self.hash_count += 1

            file.write(self.encrypt.encoder("----------------------"))
            file.write(self.encrypt.encoder(f"k:{key}"))
            file.write(self.encrypt.encoder(f"v:{value}"))
            file.write(self.encrypt.encoder(f"h:{raw_hash}"))
        
        with self.data_file.open("rb") as file:
            raw_lines = file.readlines()

        line_count = []
        for line in raw_lines:
            decrypted = self.encrypt.decode(line)
            if decrypted != False:
                line_count.append(decrypted)

        for i in range(len(line_count)):
            if line_count[i].startswith("hash-size:"):
                line_count[i] = f"hash-size: {self.hash_count}\n"

        encrypted_lines = []
        for line in line_count:
            encrypt = self.encrypt.encoder(line)
            encrypted_lines.append(encrypt)

        with self.data_file.open("wb") as file:
            file.writelines(encrypted_lines)

    def store_delete(self, key):
        self.data_file.touch()

        with self.data_file.open("ab") as file:
            if self.hash_count == 0:
                self.hash_count += 1
                file.write(self.encrypt.encoder(f"hash-size: {self.hash_count}"))
            else:
                self.hash_count -= 1

            file.write(self.encrypt.encoder("----------------------"))
            file.write(self.encrypt.encoder(f"Delete:{key}"))
    
    
# class SettingsWindow:
#     def __init__(self, parent, app):
#         self.window = tk.Toplevel(parent)
#         self.app = app
#         self.window.transient(parent) # makes child toplevel act as a dialogue box
#         self.window.grab_set() #force use window until closed (initialises 1 second after window opens)
#         self.window.focus_set() # focuses on the window 

#         self.window.title("Settings")
#         self.window.geometry(f"250x155+{self.app.x + 800}+{self.app.y + 100}")
#         self.window.config(bg="#f5f5f5")
        
#         self.window.grid_rowconfigure(0, weight=1)
#         self.window.grid_columnconfigure(0, weight=1)
        
#         content_frame = ttk.Frame(self.window)
#         content_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
#         content_frame.grid_columnconfigure(0, weight=1)
        
#         db_frame = ttk.LabelFrame(content_frame, text="Statistics", padding=15)
#         db_frame.grid(row=1, column=0, sticky="ew")
#         db_frame.grid_columnconfigure(0, weight=1)
        
#         # test = tk.StringVar(value=Pipeline().array_update)
#         ttk.Label(db_frame, text="Map size: ").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 0))
#         ttk.Label(db_frame, text="Congestion: ").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
#         ttk.Label(db_frame, text="Hash count: ").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=(10, 0))

#         Map_C_frame = ttk.Label(db_frame, text="---").grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(0, 0))
#         C_frame = ttk.Label(db_frame, text="---").grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(10, 0))
#         Hash_amount_frame = ttk.Label(db_frame, text="---").grid(row=2, column=1, sticky="w", padx=(0, 10), pady=(10, 0))

#         #keyboard mapping
#         self.window.bind("<Escape>", lambda event: self.close())

#     def close(self):
#         self.window.destroy()