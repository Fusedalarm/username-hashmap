class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value 
        self.next = None

    
class LinkedList:
    def __init__(self):
        self.head = None
       

    def append(self, key, value):

        temp_store = Node(key, value)

        if self.head == None:
            self.head = temp_store
            return self.head
        
        current = self.head
        while True:
            if current.key == temp_store.key: # make sure that keys are not identical
                print("Error - invalid key")
                return False
            
            if current.next is None:
                break

            current = current.next # keep iterating through the list until pointer is none
        
        current.next = temp_store
        return current.next
    
    def delete(self, key):
        previous = None
        current = self.head
        key_validate = True
        
        if self.head is None:
            print("error")
            return False
        
        while current != None:
            if current.key == key:
                key_validate = False
                break

            previous = current
            current = current.next # keep iterating through the list until pointer is none       
        if key_validate == True:
            return False

        if current == self.head: #delete head
            self.head = current.next
        elif current.next is None: #delete last
            previous.next = None
        else: # delete middle
            previous.next = current.next
        return True

    def retrieve(self, key):

        current = self.head
        if self.head is None:
            return False
        
        while True:
            if current.key == key: # make sure that keys are not identical
                return current
            
            if current.next is None:
                break             

            current = current.next   
        return False


    def print(self):
        current = self.head
        while current is not None:
            print(current.key, current.value)
            current = current.next


# hash = LinkedList()
# while True:
#     func_choose = int(input("enter func: "))
#     if func_choose == 1:
#         for i in range(3):       
#             buffer = input("enter value: ").strip()
#             hash.append(buffer, "test")
#         hash.print()

#     elif func_choose == 2:
#         delete_key = input("enter the key: ").strip()
#         hash.delete(delete_key)
#         hash.print()
