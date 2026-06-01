class DataStore:
    def __init__(self, dictionary_name, key, info):
        self.dictionary_name = dictionary_name
        self.key = key
        self.infor = info
    
    def dictionary_store(self):
        dictionary_name = {
            "key": self.key,
            "info": self.info
        }
    
    def dictionary_print(self):
        print(dictionary_name["key"])
        print(dictionary_name["info"])