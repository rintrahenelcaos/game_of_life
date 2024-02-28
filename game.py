from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtWidgets import QLabel, QMainWindow, QFrame, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

import numpy as np
import sys


GAME_WIDTH = 900
GAME_HEIGHT = 900
CELL_SIZE = 18
NUMBER_OF_COL = int(GAME_WIDTH/CELL_SIZE)
NUMBER_OF_ROW = int(GAME_HEIGHT/CELL_SIZE)

class Cell(QLabel):
    def __init__(self, reference_frame, xpos, ypos):
        
        changestate = pyqtSignal(bool)
        
        QLabel.__init__(self, reference_frame)
        
        self.setObjectName(str(xpos)+","+str(ypos))
        self.setGeometry(QtCore.QRect(xpos*CELL_SIZE,ypos*CELL_SIZE,CELL_SIZE,CELL_SIZE))
        self.alive = False
        
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    
        self.setMouseTracking(True)    
        
    """def mousePress(self, event):
        super().mousePressEvent(event)
        statechanged = True"""
        
    def alive_or_not(self):
        if self.alive: self.setStyleSheet("background-color: white")
        else: self.setStyleSheet("background-color: black")
        
class Main_window(QMainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        
        self.setObjectName("MainWindow")
        self.resize(1000, 900)
        self.setWindowTitle("MainWindow")
        self.setStyleSheet("QWidget { background-color: #0E0E0E}")
        self.setWindowTitle("Game of life")
        
        self.game_frame = QFrame(self)
        self.game_frame.resize(900,900)
        self.game_frame.setStyleSheet("background-color: transparent")
        
        self.evolve_button = QPushButton(self)
        self.evolve_button.setShortcut("Space")
        self.evolve_button.setGeometry(QtCore.QRect(905,10,90,50))
        self.evolve_button.clicked.connect(lambda: self.launch())
        self.evolve_button.setStyleSheet("background-color: gray")
        
        self.timer = QTimer(self)
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
    
    def life(self):
        growth(grid)
        print(grid)
        self.cell_assigner()
        
    def launch(self):
        self.evolve_button.clicked.connect(lambda: self.timer.stop())
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.life)
        self.timer.start()
        
        
    
    
        
        
grid = [[False for y in range(NUMBER_OF_ROW)] for x in range(NUMBER_OF_COL)]    # cell position: [row][col]


grid[8][3] = True
grid[8][4] = True
grid[8][5] = True
grid[8][6] = True
grid[8][7] = True
grid[8][8] = True
grid[8][9] = True
grid[9][10] = True
grid[10][10] = True
grid[11][10] = True
grid[12][10] = True
grid[13][10] = True





def neighborhood(posx, posy, habitat):
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
                if habitat[x][y]:
                    alive_neighbor += 1
    return alive_neighbor
    
def alive(posx, posy, habitat, habitatoriginal):
    near_cells = neighborhood(posx, posy, habitatoriginal)
    if habitatoriginal[posx][posy]:
        if near_cells < 2: habitat[posx][posy] = False
        elif near_cells > 3: habitat[posx][posy] = False
    else: 
        if near_cells == 3: habitat[posx][posy] = True
        
def growth(habitat):
    previous = habitat.copy()
    for x in range(NUMBER_OF_COL):
        for y in range(NUMBER_OF_ROW):
            alive(x, y, habitat, previous)
            
            
    
        

        

        
        
          
             
        

                
    
    
    
        

        

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = Main_window()
    
    ui.show()

    sys.exit(app.exec_())
        
       
        