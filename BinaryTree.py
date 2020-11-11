#This has been created starting from the root of the tree and inserting the rest of nodes recursively.
class Binary_tree:

    def __init__ (self, value):

        self.left = None
        self.right = None
        self.value = value
    

    def insert(self, value):

        if self.value: #si hay root
            if value < self.value: #y es menor
                if self.left is None: #y hay hueco
                    self.left = Binary_tree(value) #se mete
                   
                else:
                    self.left.insert(value) #si no hay hueco hace recursividad hasta que lo hay y se mete
            elif value > self.value:
                    if self.right is None:
                        self.right = Binary_tree(value)
                    else:
                        self.right.insert(value)
        else:
            self.value = value #si no hay root el value será el root  



