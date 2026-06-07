from utils.array import Array
from utils.hashfunc import Hash

class Pipeline:
    def __init__(self):
        self.hash = Hash()
        self.array = Array()

    def array_init(self):
        self.ARRAY_SIZE = 16
        self.array = self.array.array_create(self.ARRAY_SIZE)
        print("hash table initialised")

    def console_menu(self):
        self.array_init()
        print("\n=========================")
        print("1--------- input values")
        print("2--------- retrieve")
        print("3--------- exit")   

        while True:
            try:
                menu_picker = input("choose option: ")
                menu_picker = int(menu_picker)

                if menu_picker == 1:
                    self.value_input()
                elif menu_picker == 2:
                    self.retrieve_key()
                elif menu_picker == 3:
                    print("program exiting...")
                    break
                else:
                    print("invalid option")
                
            except ValueError:
                print("invalid character/s entered")
        
    def value_input(self):
        while True:
            self.key = input("input key: ")
            self.hashed_key = self.hash.hasher(self.key)
            if self.hashed_key is not None:
                break
        
        self.value = input("input value: ")
        self.store_hash()

    def store_hash(self):
        Array_index = self.hashed_key % self.ARRAY_SIZE
        start_index = Array_index
        while True:
            if self.array[Array_index][0] == 0:
                self.array[Array_index][0] = self.key
                self.array[Array_index][1] = self.value
                break
            else: 
                Array_index = (Array_index + 1) % self.ARRAY_SIZE
                if start_index == Array_index:
                    print("hash table is full")
                    break

    def retrieve_key(self):
        key = input("enter key: ")
        self.retrieval_hash = self.hash.hasher(key)
        self.retrieval_index = self.retrieval_hash % self.ARRAY_SIZE
        self.key_validate = self.array[self.retrieval_index][0]
        start_index = self.retrieval_index

        while True:
            if key == self.key_validate:
                print(self.array[self.retrieval_index][0], self.array[self.retrieval_index][1])
                break
            elif self.key_validate == 0:
                print("key does not exist")
                break
            else:
                self.retrieval_index = (self.retrieval_index + 1) % self.ARRAY_SIZE
                if start_index == self.retrieval_index:
                    print("hash table is full")
                    break 

Pipeline().console_menu()