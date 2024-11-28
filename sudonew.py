import pygame
import copy
import time  # for displaying

sudoku_inp = [
    [0, 0, 0, 0, 6, 2, 3, 0, 0],
    [3, 4, 9, 0, 1, 0, 7, 0, 0],
    [0, 5, 0, 4, 3, 0, 0, 0, 1],
    [0, 0, 2, 6, 5, 0, 0, 0, 9],
    [0, 0, 8, 0, 4, 0, 1, 6, 2],
    [0, 6, 4, 2, 9, 1, 0, 3, 8],
    [0, 0, 0, 0, 0, 6, 0, 0, 0],
    [0, 8, 0, 0, 7, 0, 0, 5, 4],
    [9, 0, 0, 3, 2, 0, 6, 0, 7],
]

class Solve:
    def __init__(self, inp):
        self.__starting_matrix = inp
        self.__matrix = copy.deepcopy(inp)
        self.__hypo_matrix = self.__makeHypoMatrix()
        self.__updateHypoMatrix()
        self.matrixPrint(self.__hypo_matrix)

    def run(self):
        self.__loneSingles()
        self.__hiddenSingles()
        self.matrixPrint(self.__hypo_matrix)
        print("\n")
        self.matrixPrint(self.__matrix)
        GUI(self.__starting_matrix, self.__matrix, self.__hypo_matrix,)

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
        pass  # shouldn't be needed because of lone singels

    def __loneSingles(self):  # only one number that can go in the cell 
        for r in range(9):
            for c in range(9):
                if len(self.__hypo_matrix[r][c]) == 1:
                    print("ls", r, c)
                    self.__matrix[r][c] = self.__hypo_matrix[r][c][0]
                    self.__updateHypoMatrix()

    def __hiddenSingles(self):  # only box a specific number can go in, but multiple numbers can go in the box
        # row
        for r in range(9):
            for n in range(9):
                n_in = []
                for c1 in range(9):
                    if n+1 in self.__hypo_matrix[r][c1]:
                        n_in.append(c1)
                if len(n_in) == 1:
                    self.__matrix[r][n_in[0]] = n+1
                    print("HIDDEN ROW")
                    self.__updateHypoMatrix()
        
        # column
        for c in range(9):
            for n in range(9):
                n_in = []
                for r1 in range(9):
                    if n+1 in self.__hypo_matrix[r1][c]:
                        n_in.append(r1)
                if len(n_in) == 1:
                    self.__matrix[n_in[0]][c] = n+1
                    print("HIDDEN COL")
                    self.__updateHypoMatrix()

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
                    self.__hypo_matrix[r][c] = []

    def __updateHypoMatrixImplicit(self):  # remove from a box when number placed near
        # row
        for r in range(9):
            for c1 in range(9):
                if self.__matrix[r][c1] != 0:
                    for c2 in range(9):
                        if self.__matrix[r][c1] in self.__hypo_matrix[r][c2]:
                            self.__hypo_matrix[r][c2].remove(self.__matrix[r][c1])
    
        # column
        for c in range(9):
            for r1 in range(9):
                if self.__matrix[r1][c] != 0:
                    for r2 in range(9):
                        if self.__matrix[r1][c] in self.__hypo_matrix[r2][c]:
                            self.__hypo_matrix[r2][c].remove(self.__matrix[r1][c])

        # box
        for bx in range(3):
            for by in range(3):
                for bx2 in range(3):
                    for by2 in range(3):
                        if self.__matrix[bx*3+bx2][by*3+by2] != 0:
                            for bx3 in range(3):
                                for by3 in range(3):
                                    if self.__matrix[bx*3+bx2][by*3+by2] in self.__hypo_matrix[bx*3+bx3][by*3+by3]:
                                        self.__hypo_matrix[bx*3+bx3][by*3+by3].remove(self.__matrix[bx*3+bx2][by*3+by2])

class GUI():
    def __init__(self, orig, fi, mat):
        print(orig)
        pygame.init()
        self.__original = orig
        self.__filled_in = fi
        self.__mat = mat
        self.__screen =  pygame.display.set_mode([825, 825])
        pygame.display.set_caption("Sudoku solver")
        self.__screen.fill("WHITE")
        self.__numberFont = pygame.font.Font(("freesansbold.ttf"), 60)
        self.__numberFontColor = (0, 0, 0)
        self.__numberFontColor2 = (255, 0, 0)
        self.__updateScreen()
        self.__showResult()

    def __showResult(self):
        self.__run = True
        self.__showGrid()
        self.__showPrefilled()
        self.__showFilled()
        self.__showMatrix()
        while self.__run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__run =False
            self.__updateScreen()
            

    def __showGrid(self):
        self.__outer_box = pygame.Rect(45, 45, 735, 735)
        self.__drawBox(self.__outer_box, "black")
        for col in range(3):
            for col2 in range(3):
                for row in range(3):
                    for row2 in range(3):
                        self.__inner_boxes = pygame.Rect(50+80*(col*3+col2)+(col*5), 50+80*(row*3+row2)+(row*5), 75, 75)
                        self.__drawBox(self.__inner_boxes, "white")

    def __showPrefilled(self):
        for col in range(3):
            for col2 in range(3):
                for row in range(3):
                    for row2 in range(3):
                        self.__number_temp = str(self.__original[row*3+row2][col*3+col2])
                        self.__numberText = self.__numberFont.render(self.__number_temp, True, self.__numberFontColor)
                        if self.__number_temp != "0":
                            self.__screen.blit(self.__numberText, (70+80*(col*3+col2)+(col*5), 60+80*(row*3+row2)+(row*5)))
                            self.__updateScreen()
        #time.sleep(0.25)

    def __showFilled(self):
        for row in range(3):
            for row2 in range(3):
                for col in range(3):
                    for col2 in range(3):
                        if self.__original[row*3+row2][col*3+col2] == 0: 
                            self.__number_temp = str(self.__filled_in[row*3+row2][col*3+col2])
                            self.__numberText = self.__numberFont.render(self.__number_temp, True, self.__numberFontColor2)
                            self.__screen.blit(self.__numberText, (70+80*(col*3+col2)+(col*5), 60+80*(row*3+row2)+(row*5)))
                            time.sleep(0.03)
                            self.__updateScreen()

    def __drawBox(self, rectd, color):
        self.__color = color
        self.__rectd = rectd
        pygame.draw.rect(self.__screen, self.__color, self.__rectd)

    def __showMatrix(self):
        self.__numpFont = pygame.font.Font(("freesansbold.ttf"), 20)
        self.__numpFontColor = (140, 140, 140)
        for row in range(3):
            for col in range(3):
                for row2 in range(3):
                    for col2 in range(3):
                        for i in range(len(self.__mat[row*3 + row2][col*3 + col2])):
                            self.__nump = self.__mat[row*3 + row2][col*3 + col2][i]
                            self.__numpText = self.__numpFont.render(str(self.__nump), True, self.__numpFontColor)
                            self.__screen.blit(self.__numpText, (60+80*(col*3+col2)+(col*5)+(((self.__nump-1)%3)*22), 57+80*(row*3+row2)+(row*5)+(((self.__nump-1)//3)*22)))
                            self.__updateScreen()
    
    def __updateScreen(self):
        pygame.display.update()
        pygame.display.flip()

sd = Solve(sudoku_inp)
sd.run()
