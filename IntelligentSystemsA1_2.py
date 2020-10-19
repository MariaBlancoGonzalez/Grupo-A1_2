import os
import sys
import numpy as np
import random
import json as js
import matplotlib.pyplot as plt

class WCell:
    RES=(16,16)
    MAX_NEIGH = 4

    def __init__(self, position):
        self.position = np.array(position)
        self.value = 0
        self.neighbors = [False for i in range(WCell.MAX_NEIGH)]

    def to_image(self):
        #Create numpy array image representation with resolution WCell.RES
        img = np.ones(WCell.RES)

        # set corners to walls
        img[0,0] = 0
        img[WCell.RES[0]-1,0] = 0
        img[0,WCell.RES[1]-1] = 0
        img[WCell.RES[0]-1,WCell.RES[1]-1] = 0

        # set wall to black
        for i in range(0, self.MAX_NEIGH):
            if not self.neighbors[i]:
                if WMaze.MOV[i][0] != 0:
                    wall = range(0,WCell.RES[1])
                    l = WCell.RES[0]-1 if WMaze.MOV[i][0] > 0 else 0
                    img[l, wall] = 0
                else:
                    wall = range(0,WCell.RES[0])
                    l = WCell.RES[1]-1 if WMaze.MOV[i][1] > 0 else 0
                    img[wall, l] = 0
        return img

class WMaze:
    # input: number of rows and columns of the maze
    MOV = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.mov = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self.id_mov = ["N", "E", "S", "O"]
        self.maze = np.array(WCell((i, j)) for i in range(rows) for j in range(cols))

        self.wilsonAlgorithmGen()

    def json_exp(self):

        path = os.getcwd()
        file = open(f"{path}/JSON_FILE.json", "w")

        row = js.dumps(self.rows)
        column = js.dumps(self.cols)
        mov = js.dumps(self.mov)
        id = js.dumps(self.id_mov)

        json = "{\n"
        json += f'"rows": {row},\n"cols": {column},\n"max_n": {WCell.MAX_NEIGH},\n"mov": {mov} ,\n"id_mov": {id},\n'
        json += '"cells": {'

        # file.write(json)
        matriz = self.matrix
        pos = ()
        number1 =0
        number2 = 0
        aux = ''
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                pos = matriz[i][j].position
                number1=pos[0]
                number2= pos[1]
                aux += "\n\t" + f'"({number1},{number2})": ' + "{" f'"value": {js.dumps(matriz[i][j].value)},"neighbors": {js.dumps(matriz[i][j].neighbors)}'+ "},"

        aux = aux[0:-1]
        print(aux)
        aux += "\n\t}\n}"

        json += aux
        file.write(f'{json}')
        file.close()

    def to_image(self):
        #Convert WMaze to a numpy array describing image
        get_pix = lambda r, c: (WCell.RES[0] * r, WCell.RES[1] * c)
        img = np.zeros(get_pix(self.rows, self.cols))

        for row in self.matrix:
            for cell in row:
                # mark cell
                pos = get_pix(*cell.position)
                img[pos[0]:pos[0] + WCell.RES[0], pos[1]:pos[1] + WCell.RES[1]] = cell.to_image()
        return img

    def __reset(self):
        #Reset matrix to empty maze state
        self.matrix = [[WCell([y, x]) for x in range(0, self.cols)] for y in range(0, self.rows)]

    def wilsonAlgorithmGen(self):
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
                    list(filter(fits_boundary, np.array(self.mov) + self.matrix[row][col].position)))

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
                side = self.mov.index(mov.tolist())
                op_side = self.mov.index((-1 * mov).tolist())
                self.matrix[row][col].neighbors[side] = True
                row, col = adj
                self.matrix[row][col].neighbors[op_side] = True


def main():
    while True:
        print(
            "Welcome to our maze program, please, choose an option:\n\t 1. Implementation of the algorithm. \n\t 2. Close program.")
        option = int(input())
        #The number of rows and columns are intialized to 1 in order to avoid problems

        positive=False
        if option == 1:
            while positive==False:
                print("Introduce value for rows")
                rows = int(input())
                print("Introduce value for columns")
                cols = int(input())
                if rows > 0 and cols > 0:
                    positive = True
                else:
                    print("Maze dimensions must be positive, type them again, please.")

            lab = WMaze(rows, cols)
            lab.json_exp()

            img = lab.to_image()
            plt.imshow(img)
            plt.show()
        elif option == 2:
            print("Have a nice day!!")
            break
        else:
            print("You pressed a wrong option... \t Press a key to continue.")

if __name__ == '__main__':
    main()
