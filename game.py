from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtWidgets import QLabel, QMainWindow, QFrame
from PyQt5.QtCore import Qt

import numpy as np
import sys


GAME_WIDTH = 900
GAME_HEIGHT = 360
CELL_SIZE = 90
NUMBER_OF_COL = int(GAME_WIDTH/CELL_SIZE)
NUMBER_OF_ROW = int(GAME_HEIGHT/CELL_SIZE)

class Cell(QLabel):
    def __init__(self, reference_frame, xpos, ypos):
        QLabel.__init__(self, reference_frame)
        
        self.setObjectName(str(xpos)+","+str(ypos))
        self.setGeometry(QtCore.QRect(xpos*CELL_SIZE,ypos*CELL_SIZE,CELL_SIZE,CELL_SIZE))
        self.alive = False
        
    def alive_or_not(self):
        if self.alive: self.setStyleSheet("background-color: white")
        else: self.setStyleSheet("background-color: black")
        
class Main_window(QMainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        
        self.setObjectName("MainWindow")
        self.resize(1000, 900)
        self.setWindowTitle("MainWindow")
        self.setStyleSheet("QWidget { background-color: black}")
        self.setWindowTitle("Game of life")
        
        self.game_frame = QFrame(self)
        self.game_frame.resize(900,900)
        self.game_frame.setStyleSheet("background-color: red")
        
        self.cell_creator()
        
        self.cell_assigner()
        
    def cell_creator(self):
        
        for x in range(NUMBER_OF_COL):
            for y in range(NUMBER_OF_ROW):
                Cell(self.game_frame, x, y)
    
    def cell_assigner(self):
        
        for y in range(NUMBER_OF_ROW):
            for x in range(NUMBER_OF_COL):
                one_cell = self.game_frame.findChild(Cell, str(x)+","+str(y))
                one_cell.alive = grid[x][y]
                one_cell.alive_or_not()
    
    
        
        
grid = [[False for y in range(NUMBER_OF_ROW)] for x in range(NUMBER_OF_COL)]    # cell position: [row][col]
print(grid)

grid[8][3] = True



def neighborhood(posx, posy):
    alive_neighbor = 0
    
    if posx == 0:
        ontheleft=posx
    else: ontheleft = posx-1
    if posx == NUMBER_OF_COL-1:
        ontheright = posx+1
    else: ontheright = posx+2
    
    if posy == 0:
        ontop=posy
    else: ontop = posy-1
    if posy == NUMBER_OF_ROW-1:
        onbottom = posy+1
    else: onbottom = posy+2
    
    
    for x in range(ontheleft,ontheright):
        for y in range(ontop,onbottom):
            if x == posx and y == posy:
                pass
            else: 
                if grid[x][y]:
                    alive_neighbor += 1
    return alive_neighbor
    
def alive(posx, posy):
    near_cells = neighborhood(posx, posy)
    if grid[posx][posy]:
        if near_cells < 2: grid[posx][posy] = False
        elif near_cells > 3: grid[posx][posy] = False
    else: 
        if near_cells == 3: grid[posx][posy] = True
        
print(neighborhood(7,3))
        

        
        
          
             
        

                
    
    
    
        

        

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = Main_window()
    
    ui.show()

    sys.exit(app.exec_())
        
       
        