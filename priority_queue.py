#PRIORITY QUEUE CLASS IMPLEMENTATION (UNFINISHED)

class Node:
    """Node(obj)\nobj - data object\n
    Priority Queue node element"""

    def __init__(self, obj):
        self.obj = obj
        self.forward = None

    def get(self):
        return self.obj


class PriorityQueue(object):
    #Inicialization of the queue
    def __init__(self):
        self.queue = []
        self.length = 0
    
    #ToString
    def __str__(self):
        return ' '.join(str[i] for i in self.queue)

    def __len__(self):
        return self.length
    
    def __getItem__(self, item):
        #revisar si 100% esto funciona en colas tb
        return self.get[item]

    def __getNode__(self,node):
        #complete
        return node   
    
    #Inserting
    def __insert__(self, node):
        return self.queue.append(node)
    
    #Popping elements
    def __delete__(self):
        max = 0
        try:
            for i in range(len(self.queue)):
                if (self.queue[i] > self.queue[max]):
                    max = i
                
                data = self.queue[max]
                del self.queue[max]
            return data
        except IndexError:
            print("Index Error")
            exit()
        

