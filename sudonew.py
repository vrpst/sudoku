import pygame
import copy
import time  # for displaying

sudoku_inp = [
    [0, 2, 7, 8, 0, 0, 0, 0, 9],
    [0, 0, 4, 0, 0, 0, 5, 3, 0],
    [0, 6, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 5, 7, 4, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 1, 0],
    [9, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 5, 0, 0, 2],
    [0, 0, 0, 7, 0, 0, 0, 0, 5],
    [0, 0, 1, 0, 2, 0, 0, 7, 0],
]

class Solve:
    def __init__(self, inp):
        self.__starting_matrix = inp
        self.__matrix = copy.deepcopy(inp)
        self.__hypo_matrix = self.__makeHypoMatrix()
        self.__updateHypoMatrix()

    def matrixPrint(self, inp):
        for i in inp:
            print(i)
    
    def __makeHypoMatrix(self):
        hypomat = []
        for i in range(9):
            hypomat.append([])
            for j in range(9):
                hypomat[i].append([1, 2, 3, 4, 5, 6, 7, 8, 9])
        return hypomat

    def __openSingles(self):  # all boxes filled but that one
        pass

    def __loneSingles(self):  # only one number that can go in the box 
        for r in range(9):
            for c in range(9):
                if len(self.__hypo_matrix[r][c]) == 0:
                    self.__matrix[r][c] = self.__hypo_matrix[r][c][0]
                    self.__updateHypoMatrix()

    def __hiddenSingles(self):  # only box a specific number can go in, but multiple numbers can go in the box
        pass

    def __nakedPairs(self):  # two boxes with only one and the same pair of numbers that can go in
        pass

    def __hiddenPairs(self):  # only two boxes a pair of numbers can go in, but other numbers can go there as well
        pass

    def __ommision(self):  # use the limitations of a hypothetical to eliminate itself elsewhere
        pass

    def __updateHypoMatrix(self):  # update hypo_matrix to reflect numbers filled etc
        self.__updateHypoMatrixExplicit()
        self.__updateHypoMatrixImplicit()

    def __updateHypoMatrixExplicit(self):  # clear a box when it is filled
        for r in range(9):
            for c in range(9):
                if self.__matrix[r][c] != 0:
                    print(self.__hypo_matrix[r][c])
                    self.__hypo_matrix[r][c] = []

    def __updateHypoMatrixImplicit(self):  # remove from a box when number placed near
        # row
        for r in range(9):
            for c1 in range(9):
                for n in range(9):
                    if n+1 == self.__matrix[r][c1]:
                        for c2 in range(9):
                            if n+1 in self.__hypo_matrix[r][c2]:
                                print(r, n)
                                self.__hypo_matrix[r][c2].remove(n+1)
        # column
        for c in range(9):
            for r1 in range(9):
                for n in range(9):
                    if n+1 == self.__hypo_matrix[r1][c]:
                        for r2 in range(9):
                            if n+1 in self.__hypo_matrix[r2][c]:
                                self.__hypo_matrix[r2][c].remove(n+1)

        # box
        for bx in range(3):
            for by in range(3):
                for bx2 in range(3):
                    for by2 in range(3):
                        for n in range(9):
                            if n+1 == self.__matrix[bx*3+bx2][by*3+by2]:
                                for bx3 in range(3):
                                    for by3 in range(3):
                                        if n+1 in self.__hypo_matrix[bx*3+bx3][by*3+by3]:
                                            self.__hypo_matrix[bx*3+bx3][by*3+by3].remove(n+1)
        
        self.matrixPrint(self.__hypo_matrix)

Solve(sudoku_inp)