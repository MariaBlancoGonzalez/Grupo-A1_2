import sys
import random
import numpy as np
import matplotlib.pyplot as plt

class WCell:
    """
    WCell(row, col)\n
    Maze cell class
    """

    MAX_N = 4

    def __init__(self, position):
        self.value = 0
        self.position = np.array(position)
        self.neighbors = [False for _ in range(WCell.MAX_N)]

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
    Maze class with Wilson's generator
    """

    CLR_CELL = 255
    CLR_CONN = 220
    ID_MOV = ["N", "E", "S", "O"]
    MOV = [[-1,0], [0,1], [1,0], [0,-1]]

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = None

        # initial generation
        self.generate()

    def __reset(self):
        "Reset matrix to empty maze state"
        self.matrix = [[WCell([y, x]) for x in range(0, self.cols)] for y in range(0, self.rows)]

    def generate(self):
        "Generate maze using Wilson's algorithm"
        self.__reset()
        if self.rows < 1 or self.cols < 1:
            return

        # initialize
        fits_boundary = lambda i: i[0] >= 0 and i[0] < self.rows and i[1] >= 0 and i[1] < self.cols
        visited = [[False for x in range(0, self.cols)] for y in range(0, self.rows)]
        free = [(y, x) for x in range(0, self.cols) for y in range(0, self.rows)]
        # set first random cell
        visited[random.randint(0, self.rows -1)][random.randint(0, self.cols -1)] = True

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
                row, col = random.choice(list(filter(fits_boundary, np.array(self.MOV) + self.matrix[row][col].position)))

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

    def to_image(self):
        "Convert WMaze to a numpy array describing image"
        get_pix = lambda r, c: (r * 2 + 1, c * 2 + 1)
        img = np.zeros(get_pix(self.rows, self.cols))

        for row in self.matrix:
            for cell in row:
                # mark cell
                pix = np.array(get_pix(*cell.position))
                img[pix[0]][pix[1]] = self.CLR_CELL

                # open walls
                sides = cell.neighbors
                for i in range(0, len(sides)):
                    if sides[i]:
                        npix = pix + np.array(self.MOV[i])
                        img[npix[0]][npix[1]] = self.CLR_CONN
        return img

    def to_json(self):
        "Convert WMaze to json string"
        json = "{\n"
        maxn = self.matrix[0][0].MAX_N
        json += f'"rows": {self.rows},\n"cols": {self.cols},\n"max_n": {maxn},\n"mov": {self.MOV},\n"id_mov": {self.ID_MOV},\n'
        json += '"cells": {\n'

        c_json = ""
        for r in self.matrix:
            for x in r:
                c_json += str(x) + ",\n"
        json += c_json[:-2] + "\n}\n}"
        return json

    @staticmethod
    def from_json(json):
        """
        Load WMaze from json string\n
        Preserves global static attributes
        """
        json = eval(json.replace('f', 'F').replace('t', 'T'))

        # save MAX_N current value
        maxn = WCell.MAX_N
        WCell.MAX_N = json['max_n']

        m = WMaze(0, 0)
        m.rows = json['rows']
        m.cols = json['cols']
        m.MOV = json['mov']
        m.ID_MOV = json['id_mov']
        m.__reset()
        cells = json['cells']
        for key in cells:
            k = eval(key)
            m.matrix[k[0]][k[1]].value = cells[key]['value']
            m.matrix[k[0]][k[1]].neighbors = cells[key]['neighbors']

        # restore MAX_N value
        WCell.MAX_N = maxn

        return m

def main():
    r = 10
    c = 10
    if len(sys.argv) > 1:
        r = int(sys.argv[1])
        if len(sys.argv) > 2:
            c = int(sys.argv[2])
    maze = WMaze(r, c)
    img = maze.to_image()
    plt.imshow(img)
    plt.show()

if __name__ == '__main__':
    main()
