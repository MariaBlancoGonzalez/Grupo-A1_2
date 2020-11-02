from linkedlist import LinkedList
import os
import numpy as np
import random
import json as js
import matplotlib.pyplot as plt

class WCell:
    """
    WCell(position_vector)\n
    Maze cell class
    """

    RES=(16,16)
    MAX_NEIGH = 4

    def __init__(self, position):
        self.position = np.array(position)
        self.value = 0
        self.neighbors = [False for i in range(WCell.MAX_NEIGH)]

    def to_image(self):
        "Create numpy array image representation with resolution WCell.RES"
        # Set image to white
        img = np.ones(WCell.RES) * 255

        # set corners to walls (black color)
        img[0,0] = 0
        img[WCell.RES[0]-1,0] = 0
        img[0,WCell.RES[1]-1] = 0
        img[WCell.RES[0]-1,WCell.RES[1]-1] = 0

        # iterate walls
        for i in range(0, self.MAX_NEIGH):
            # if there is wall
            if not self.neighbors[i]:
                # N-S axle
                if WMaze.MOV[i][0] != 0:
                    pixel_wall = range(0,WCell.RES[1])
                    pixel_row = WCell.RES[0]-1 if WMaze.MOV[i][0] > 0 else 0
                    img[pixel_row, pixel_wall] = 0
                # O-E axle
                else:
                    pixel_wall = range(0,WCell.RES[0])
                    pixel_col = WCell.RES[1]-1 if WMaze.MOV[i][1] > 0 else 0
                    img[pixel_wall, pixel_col] = 0
        return img

    def to_dict(self):
        return {'value': self.value, 'neighbors': self.neighbors}

    def __str__(self):
        pos = str(self.position.tolist())[1:-1]
        return f'"({pos})": ' + str(self.to_dict()).lower()

    def __repr__(self):
        return str(self)

class WMaze:
    """
    WMaze(rows, cols)\n
    input: number of rows and columns of the maze\n\n
    Maze class with Wilson's generator
    """

    ID_MOV = ["N", "E", "S", "O"]
    MOV = [[-1, 0], [0, 1], [1, 0], [0, -1]]

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.wilsonAlgorithmGen()

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
        img = np.zeros(get_pix(self.rows, self.cols))

        for row in self.matrix:
            for cell in row:
                # mark cell
                pos = get_pix(*cell.position)
                img[pos[0]:pos[0] + WCell.RES[0], pos[1]:pos[1] + WCell.RES[1]] = cell.to_image()
        return img

    def __reset(self):
        "Reset matrix to empty maze state"
        self.matrix = [[WCell([y, x]) for x in range(0, self.cols)] for y in range(0, self.rows)]

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

def main():
    while True:
        print("""Welcome to our maze program, please, choose an option: \n\t
        1. Run the algorithm. \n\t
        2. Close program.""")
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

            img = lab.to_image()
            plt.imshow(img)
            plt.show()
        elif option == 2:
            print("Exiting program...")
            break
        else:
            print("You pressed a wrong option... \t Press a key to continue.")

if __name__ == '__main__':
    main()
