from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtWidgets import QLabel, QMainWindow
from PyQt5.QtCore import Qt

import numpy as np
import sys


GAME_WIDTH = 900
GAME_HEIGHT = 900
CELL_SIZE = 50
NUMBER_OF_COL = int(GAME_WIDTH/CELL_SIZE)
NUMBER_OF_ROW = int(GAME_HEIGHT/CELL_SIZE)

class Cell(QLabel):
    def __init__(self, reference_frame, xpos, ypos):
        QLabel.__init__(self, reference_frame)
        
        
        self.setGeometry(QtCore.QRect(xpos,ypos,CELL_SIZE,CELL_SIZE))
        self.setStyleSheet("background-color: white")
        
class Main_window(QMainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        
        self.setObjectName("MainWindow")
        self.resize(900, 900)
        self.setWindowTitle("MainWindow")
        self.setStyleSheet("QWidget { background-color: black}")
        self.setWindowTitle("Game of life")
        
        Cell(self, 50, 100)
        
grid = [[False for x in range(NUMBER_OF_COL)] for y in range(NUMBER_OF_ROW)]    # cell position: [row][col]
print(grid)

def neighborhood(posx, posy):
    alive_neighbor = 0
    
    if posx == 0:
        ontheleft=posx
    else: ontheleft = posx-1
    if posx == NUMBER_OF_COL:
        ontheright = posx+1
    else: ontheright = posx+2
    
    if posy == 0:
        ontop=posy
    else: ontop = posy-1
    if posy == NUMBER_OF_ROW:
        onbottom = posy+1
    else: onbottom = posy+2
    
    
    for x in range(ontheleft,ontheright):
        for y in range(ontop,onbottom):
            if grid[x][y]:
                alive_neighbor += 1
                
    
    
    
        

        

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = Main_window()
    
    ui.show()

    sys.exit(app.exec_())
        
       
        