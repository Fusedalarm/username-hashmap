class Array:
    @staticmethod
    def array_create(ARRAY_SIZE): #will lose an array once it has been created when resizing eg
        outer_list = []

        for i in range(ARRAY_SIZE):
            inner_list = []
            for j in range(2):
                inner_list.append(0)
            outer_list.append(inner_list)
        
        return outer_list

        


    