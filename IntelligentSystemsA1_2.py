#!/usr/bin/python
from heap import Heap
from vector import SortedVector
from binarysearch import bisection
import os
import numpy as np
import random
import json as js
import PIL.Image

class WCell:
    """
    WCell(position_vector, value)

    - position_vector -- iterable coordinates
    - value -- int cell type (travel cost)

    Maze cell class
    """
    COLORS = {0:(255,255,255), 1:(245,220,180), 2:(150,250,150), 3:(130,200,250)}
    SPECIAL_CLR = (255,0,0)
    RES = (16,16)
    MAX_NEIGH = 4

    def __init__(self, position, val=0):
        self.position = np.array(position)
        self.value = val
        self.neighbors = [False for i in range(WCell.MAX_NEIGH)]
        self.is_solution = False
        self.is_tree = False

    def cost(self):
        return self.value + 1

    def to_image(self):
        "Create numpy array image representation with resolution WCell.RES"
        # Set image to white
        if self.is_solution or self.is_tree:
            clr = self.SPECIAL_CLR
        else:
            clr = self.COLORS[self.value]
        img = np.ones((*WCell.RES, 1)) * clr

        # set corners to walls (black color)
        img[0,0] = np.zeros(3)
        img[WCell.RES[0]-1,0] = np.zeros(3)
        img[0,WCell.RES[1]-1] = np.zeros(3)
        img[WCell.RES[0]-1,WCell.RES[1]-1] = np.zeros(3)

        # iterate walls
        for i in range(0, self.MAX_NEIGH):
            # if there is wall
            if not self.neighbors[i]:
                # N-S axle
                if WMaze.MOV[i][0] != 0:
                    pixel_wall = range(0,WCell.RES[1])
                    pixel_row = WCell.RES[0]-1 if WMaze.MOV[i][0] > 0 else 0
                    img[pixel_row, pixel_wall] = np.zeros(3)
                # O-E axle
                else:
                    pixel_wall = range(0,WCell.RES[0])
                    pixel_col = WCell.RES[1]-1 if WMaze.MOV[i][1] > 0 else 0
                    img[pixel_wall, pixel_col] = np.zeros(3)
        return img.astype('uint8')

    def to_dict(self):
        return {'value': self.value, 'neighbors': self.neighbors}

    def __str__(self):
        pos = str(self.position.tolist())[1:-1]
        return f'"({pos})": ' + str(self.to_dict()).lower()

    def __repr__(self):
        return str(self)

class WMaze:
    """
    WMaze(rows, cols, filedata=None)

    Maze class with Wilson's generator

    Arguments:
    - rows -- number of rows
    - cols -- number of columns
    - filedata -- (optional) json maze file path
    """

    ID_MOV = ["N", "E", "S", "O"]

    MOV = [[-1, 0], [0, 1], [1, 0], [0, -1]]

    def __init__(self, rows, cols, filedata=None):
        self.rows = rows
        self.cols = cols
        # In the first case, we receive the rows and columns from the user.
        if filedata is None:
            self.wilsonAlgorithmGen()
        # In the second case, we receive the rows, the columns from the .json file passed.
        else:
            self.from_json_file(filedata)

    def get(self, row, col):
        """
        Get WCell at given maze location.

        Returns: WCell
        """
        return self.matrix[row][col]

    def succesor_fn(self, state):
        """
        Generate succesors of a given state

        Returns a list of (mov, state, cost)
        """
        cell = self.matrix[state[0]][state[1]]
        succesors = []
        for i in range(0, cell.MAX_NEIGH):
            if cell.neighbors[i]:
                succesor_state = tuple(np.array(self.MOV[i]) + cell.position)
                succesors.append((self.ID_MOV[i], succesor_state, cell.cost()))
        return succesors

    def to_json(self):
        "Convert maze to a json string"
        row = js.dumps(self.rows)
        column = js.dumps(self.cols)
        mov = js.dumps(self.MOV)
        idm = js.dumps(self.ID_MOV)

        json = "{\n"
        json += f'"rows": {row},\n"cols": {column},\n"max_n": {WCell.MAX_NEIGH},\n"mov": {mov} ,\n"id_mov": {idm},\n'
        json += '"cells": {'

        #maze cells
        matriz = self.matrix
        pos = ()
        number1 =0
        number2 = 0
        aux = ''
        #extracting elements for each cell and dump
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                pos = matriz[i][j].position
                number1=pos[0]
                number2= pos[1]
                aux += "\n\t" + f'"({number1},{number2})": ' + "{" f'"value": {js.dumps(matriz[i][j].value)},"neighbors": {js.dumps(matriz[i][j].neighbors)}'+ "},"

        #delete the last ','
        aux = aux[0:-1]
        aux += "\n\t}\n}"
        json += aux
        return json

    def json_exp(self, filename="maze.json"):
        "Save json represantation of the maze to a file"
        jfile = open(filename, "w")
        #write json file
        jfile.write(self.to_json())
        jfile.close()

    def to_image(self):
        "Convert WMaze to a numpy array describing image"
        get_pix = lambda r, c: (WCell.RES[0] * r, WCell.RES[1] * c)
        img = np.zeros((*get_pix(self.rows, self.cols), 3))

        for row in self.matrix:
            for cell in row:
                # mark cell
                pos = get_pix(*cell.position)
                img[pos[0]:pos[0] + WCell.RES[0], pos[1]:pos[1] + WCell.RES[1]] = cell.to_image()
        return img.astype('uint8')

    def __reset(self):
        "Reset matrix to empty maze state"
        self.matrix = [[WCell([y, x], random.randint(0,3)) for x in range(0, self.cols)] for y in range(0, self.rows)]

    def wilsonAlgorithmGen(self):
        "Generate maze using Wilson's algorithm"
        self.__reset()
        if self.rows < 1 or self.cols < 1:
            return
        # initialize
        fits_boundary = lambda i: i[0] >= 0 and i[0] < self.rows and i[1] >= 0 and i[1] < self.cols
        visited = [[False for x in range(0, self.cols)] for y in range(0, self.rows)]
        free = [(y, x) for x in range(0, self.cols) for y in range(0, self.rows)]
        # set first random cell
        visited[random.randint(0, self.rows - 1)][random.randint(0, self.cols - 1)] = True

        # iterate
        while len(free) > 0:
            walk = []
            row, col = free.pop(random.randint(0, len(free) - 1))

            # get walk path
            stop = False
            while not stop:
                if visited[row][col]:
                    stop = True
                pair = (row, col)
                if pair in walk:
                    # remove loop
                    walk = walk[:walk.index(pair)]
                walk.append(pair)
                row, col = random.choice(
                    list(filter(fits_boundary, np.array(self.MOV) + self.matrix[row][col].position)))

            # follow path and build maze
            row, col = walk[0]
            for i in range(1, len(walk)):
                visited[row][col] = True
                adj = walk[i]
                try:
                    free.remove(adj)
                except ValueError:
                    pass
                mov = np.array(adj) - self.matrix[row][col].position
                side = self.MOV.index(mov.tolist())
                op_side = self.MOV.index((-1 * mov).tolist())
                self.matrix[row][col].neighbors[side] = True
                row, col = adj
                self.matrix[row][col].neighbors[op_side] = True
                
    def from_json_file(self, data):
        """In this method we read the json file in order to retreive the most important information from it.\n
        These are the value and neighbors variable from each cell, so that we can print the maze."""
        
        with open(data, 'r') as f:
            data = js.loads(f.read())

        self.rows = data['rows']
        self.cols = data['cols']
        self.ID_MOV = data['id_mov']
        self.MOV = data['mov']

        tmp = WCell.MAX_NEIGH
        WCell.MAX_NEIGH = data['max_n']
        self.__reset()
        WCell.MAX_NEIGH = tmp

        for i in data['cells']:
            r,c = i[1:-1].split(',')
            self.matrix[int(r)][int(c)].value = data['cells'][i]['value']
            self.matrix[int(r)][int(c)].neighbors = data['cells'][i]['neighbors']

class STNode:
    """
    STNode(depth, cost, state, parent, action, heuristic, value)

    - state -- (row, col)

    SearchTree Node implementation.
    """
    IDC = 0
    def __init__(self, depth, cost, state, parent, action, heuristic, value):
        self.id = STNode.IDC
        STNode.IDC += 1
        self.depth = depth
        self.cost = cost
        self.state = state  #tupla de estado (celda), desde initial
        self.parent = parent
        if self.parent is not None:
            self.id_parent = parent.id
        else:
            self.id_parent = None
        self.action = action
        self.heuristic = heuristic
        self.value = value

    def __str__(self):
        # [<ID>][<COST>,<ID_STATE>,<ID_PARENT>,<ACTION>,<DEPTH>,<HEURISTIC>,<VALUE>]
        return f"[{self.id}][{self.cost},{self.state},{self.id_parent},{self.action},{self.depth},{self.heuristic},{self.value}]"

    def __int__(self):
        return int(self.value)

    def __gt__(self, other):
        # order by [value][row][col][id]
        if type(other) is STNode:
            if self.id == other.id:
                return False
            else:
                return not (self < other)
        else:
            return self.value > other

    def __lt__(self, other):
        # order by [value][row][col][id]
        if type(other) is STNode:
            As = (self.value, self.state[0], self.state[1], self.id)
            Bs = (other.value, other.state[0], other.state[1], other.id)
            for a,b in zip(As, Bs):
                if a == b:
                    continue
                return a < b
            return False
        else:
            return self.value < other
    
    def __eq__(self, other):
        # same state nodes are equal
        if type(other) is STNode:
            return self.state == other.state
        else:
            return self.state == other

    def __repr__(self):
        return str(self)

class Problem:
    """
    Problem(initial_state: tuple, objective_state: tuple, maze: WMaze)

    Load and solve search tree problem.

    Settings:
    - CFRONT -- frontier structure implementing push and pop
    - ALGORITHM -- algorithm type (BREADTH, DEPTH, UNIFORM, GREEDY, 'A)
    - LIMIT -- maximum tree depth
    """
    CFRONT = Heap
    ALGORITHM = 'BREADTH'
    LIMIT = 1000000

    def __init__(self, init: tuple, obj: tuple, maze: WMaze):
        self.initial = init
        self.objective = obj
        self.maze = maze
        self.frontier = None
        self.visited = None

    def solve(self):
        """
        Build search tree and find solution path
        
        Returns: solution STNode
        """
        # reinit frontier
        self.frontier = self.CFRONT()

        solution = None
        if self.ALGORITHM == 'DEPTH':
            reached_depth = 0
            i = 0
            while solution is None:
                solution, d = self._solve(i)

                # early stopping if cannot expand deeper
                if reached_depth == d:
                    break
                else:
                    reached_depth = d

                i += 1
        else:
            solution = self._solve()[0]

        if solution is not None:
            self.updateMaze(solution)
        return solution

    def _solve(self, limit=None):
        """
        Solve problem until given depth limit.

        Returns: (solution, depth) tuple
        """
        self.visited = SortedVector()
        maxdepth = 0

        if limit is None:
            limit = self.LIMIT

        # root element
        h = self.heuristic(self.initial)
        value = self.algorithmValue(0, 0, h)
        root = STNode(0, 0, self.initial, None, None, h, value)
        self.frontier.push(root)

        solution = None
        while len(self.frontier) > 0:
            nodo = self.frontier.pop()

            self.visited.push(nodo.state)

            if self.goal(nodo.state):
                solution = nodo
                break

            maxdepth += 1
            for s in self.maze.succesor_fn(nodo.state):
                h = self.heuristic(s[1])
                depth = nodo.depth + 1
                if depth > limit:
                    break
                cost = nodo.cost + s[2]
                value = self.algorithmValue(depth, cost, h)

                successor = STNode(depth, cost, s[1], nodo, s[0], h, value)

                index = bisection(self.visited, successor.state, 0, len(self.visited))
                if len(self.visited) <= index or successor != self.visited[index]:
                    self.frontier.push(successor)

        return solution, maxdepth

    def cleanMaze(self):
        "Reset maze cells flags"
        for row in self.maze.matrix:
            for c in row:
                c.is_solution = False
                c.is_tree = False

    def updateMaze(self, solution: STNode):
        """
        Set maze cells flags to correctly display solution.
        """
        self.cleanMaze()
        for s in self.visited:
            c = self.maze.get(*s)
            c.is_tree = True
            c.SPECIAL_CLR = (0,255,0)
        for n in self.frontier:
            c = self.maze.get(*n.state)
            c.is_tree = True
            c.SPECIAL_CLR = (0,0,255)
        while solution is not None:
            c = self.maze.get(*solution.state)
            c.is_solution = True
            c.SPECIAL_CLR = (255,0,0)
            solution = solution.parent

    def algorithmValue(self, depth, cost, heuristic):
        if self.ALGORITHM == 'BREADTH':
            return depth
        elif self.ALGORITHM == 'DEPTH':
            return -depth
        elif self.ALGORITHM == 'UNIFORM':
            return cost
        elif self.ALGORITHM == 'GREEDY':
            return heuristic
        elif self.ALGORITHM == "'A":
            return cost + heuristic
        return None

    def heuristic(self, state: tuple):
        """
        Calculate heuristic using manhattan distance
        """
        heuristic = abs(state[0] - self.objective[0]) + abs(state[1] - self.objective[1])
        return heuristic

    def goal(self, state):
        "Check if current state is the goal state"
        return tuple(state) == self.objective

    @staticmethod
    def from_json(fn='problem.json'):
        with open(fn, 'r') as pfile:
            json = pfile.read()
        data = eval(json)
        # ignore case and load the values
        for k in data:
            if k.lower() == 'initial':
                txt = data[k].replace(' ','').replace('(','').replace(')','').split(',')
                initial = tuple(int(x) for x in txt)
            elif k.lower().replace('c','') == 'objetive':
                txt = data[k].replace(' ','').replace('(','').replace(')','').split(',')
                objective = tuple(int(x) for x in txt)
            elif k.lower() == 'maze':
                maze_file = os.path.join(os.path.dirname(fn), data[k])
        return Problem(initial, objective, WMaze(1,1,maze_file))

def main():
    while True:
        print("""Welcome to our maze program, please, choose an option: \n\t
        1. Run the algorithm. \n\t
        2. Read .json file. \n\t
        3. Close program.""")
        option = int(input())
        #The number of rows and columns are intialized to 1 in order to avoid problems

        positive=False
        if option == 1:
            while positive==False:
                print("Introduce value for rows")
                rows = int(input())
                print("Introduce value for columns")
                cols = int(input())
                if rows > 1 and cols > 1:
                    positive = True
                else:
                    print("Maze dimensions must higher than 1, type them again, please.")

            lab = WMaze(rows, cols)
            print(f'Json file has been created in {os.getcwd()}\n')
            lab.json_exp()

            img = PIL.Image.fromarray(lab.to_image())
            img.show()
        elif option == 2:
            lab = WMaze(1, 1, input('Filepath: '))
            img = PIL.Image.fromarray(lab.to_image())
            img.show()

        elif option == 3:
            print("Exiting program...")
            break
        else:
            print("You pressed a wrong option... \t Press a key to continue.")

if __name__ == '__main__':
    main()
