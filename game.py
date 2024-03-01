from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtWidgets import QLabel, QMainWindow, QFrame, QPushButton, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

import functools
import sys


GAME_WIDTH = 900
GAME_HEIGHT = 900
CELL_SIZE = 18
NUMBER_OF_COL = int(GAME_WIDTH/CELL_SIZE)
NUMBER_OF_ROW = int(GAME_HEIGHT/CELL_SIZE)

grid = [[False for y in range(NUMBER_OF_ROW)] for x in range(NUMBER_OF_COL)]    

class Cell(QLabel):
    def __init__(self, reference_frame, xpos, ypos):
        
        changestate = pyqtSignal(bool)
        
        QLabel.__init__(self, reference_frame)
        
        self.setObjectName(str(xpos)+","+str(ypos))
        self.setGeometry(QtCore.QRect(xpos*CELL_SIZE,ypos*CELL_SIZE,CELL_SIZE,CELL_SIZE))
        self.alive = False
        
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    
        self.setMouseTracking(True)  
        
    
    def pressed(self):
        print("event") 
        
    def mousePressEvent(self, QMouseEvent):
        super(Cell, self).mousePressEvent(QMouseEvent)
        print("pressed "+self.objectName())  
        print("column "+self.objectName()[:self.objectName().find(",")])
        print("row "+self.objectName()[self.objectName().find(",")+1:])
        grid[int(self.objectName()[:self.objectName().find(",")])][int(self.objectName()[self.objectName().find(",")+1:])] = not grid[int(self.objectName()[:self.objectName().find(",")])][int(self.objectName()[self.objectName().find(",")+1:])]
        self.alive = not self.alive
        self.alive_or_not()
    
    def initial_setup(self):
        if self.alive: self.setStyleSheet("background-color: white")
        else: self.setStyleSheet("background-color: black")
    
    def alive_or_not(self):
        if self.alive: 
            apply_color_animation(self, QtGui.QColor("black"), QtGui.QColor("white"), duration=500)
            
        else: 
            apply_color_animation(self, QtGui.QColor("white"), QtGui.QColor("black"), duration=500)
            
   
        
class Main_window(QMainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        
        self.setObjectName("MainWindow")
        self.resize(1000, 900)
        self.setWindowTitle("MainWindow")
        self.setStyleSheet("background-color: dimgray")
        self.setWindowTitle("Game of life")
        
        self.game_frame = QFrame(self)
        self.game_frame.resize(900,900)
        self.game_frame.setStyleSheet("background-color: black")
        
        self.evolve_button = QPushButton(self)
        self.evolve_button.setShortcut("Space")
        self.evolve_button.setGeometry(QtCore.QRect(905,10,90,50))
        self.evolve_button.released.connect(lambda: self.launch())
        self.evolve_button.setStyleSheet("background-color: darkgreen")
        self.evolve_button.setText("Start Simulation")
        
        self.clear_button = QPushButton(self)
        self.clear_button.setText("Clear all cells")
        self.clear_button.setStyleSheet("background-color: gold")
        self.clear_button.setGeometry(QtCore.QRect(905,80,90,50))
        self.clear_button.clicked.connect(lambda: self.cleaner())
        
        self.cycle_counter = 0
        
        self.cycles = QLabel(self)
        self.cycles.setText("cycles: "+str(self.cycle_counter))
        self.cycles.setGeometry(905, 140, 90, 40)
        self.cycles.setStyleSheet("color: red")
        
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.life)
        
        self.cell_creator()
        
        self.isalive = True
        
        
    def cell_creator(self):
        
        for x in range(NUMBER_OF_COL):
            for y in range(NUMBER_OF_ROW):
                Cell(self.game_frame, x, y)
    
                    
    def cell_assigner(self, tochange):
        
        for uniquecell in tochange:
            one_cell = self.game_frame.findChild(Cell, uniquecell)
            print(int(uniquecell[:uniquecell.find(",")]))
            one_cell.alive = grid[int(uniquecell[:uniquecell.find(",")])][int(uniquecell[uniquecell.find(",")+1:])]
            one_cell.alive_or_not()
     
    def life(self):
        changed = growth(grid)
        self.cell_assigner(changed)
        self.cycle_counter += 1
        self.cycles.setText("cycles: "+str(self.cycle_counter))
        
    def launchor(self):
           
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.life)
        self.timer.start()
        
    def launch(self):
           
        if self.isalive:
            self.isalive = False
            print(self.isalive)
            self.timer.start()
            self.evolve_button.setText("Stop Simulation")
            self.evolve_button.setStyleSheet("background-color: darkred")
            
        else: 
            self.isalive = True
            print(self.isalive)
            self.timer.stop()
            self.evolve_button.setText("Start Simulation")
            self.evolve_button.setStyleSheet("background-color: darkgreen")
            
    def cleaner(self):
        self.timer.stop()
        clear()
        for y in range(NUMBER_OF_ROW):
            for x in range(NUMBER_OF_COL):
                one_cell = self.game_frame.findChild(Cell, str(x)+","+str(y))
                one_cell.alive = grid[x][y]
                one_cell.initial_setup()
        self.cycle_counter = 0
        self.cycles.setText("cycles: "+str(self.cycle_counter))
        self.isalive = True
        self.evolve_button.setText("Start Simulation")
        self.evolve_button.setStyleSheet("background-color: darkgreen")
    
    
 
def clear():
    for col in range(NUMBER_OF_COL):
        for row in range(NUMBER_OF_ROW):
            grid[col][row] = False
          

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
    status_change_indicator = str
    near_cells = neighborhood(posx, posy, habitatoriginal)
    if habitatoriginal[posx][posy]:
        if near_cells < 2: 
            habitat[posx][posy] = False
            status_change_indicator = str(posx)+","+str(posy)
        elif near_cells > 3: 
            habitat[posx][posy] = False
            status_change_indicator = str(posx)+","+str(posy)
        else: status_change_indicator = ""    
    else: 
        if near_cells == 3: 
            habitat[posx][posy] = True
            status_change_indicator = str(posx)+","+str(posy)
        else: status_change_indicator = "" 
    return status_change_indicator

def growth(habitat):
    previous = habitat.copy()
    changed_status = []
    for x in range(NUMBER_OF_COL):
        for y in range(NUMBER_OF_ROW):
            changed_status.append(alive(x, y, habitat, previous))
    changed_set = set(changed_status)
    changed_set.remove("")
    print(changed_set)   
    return changed_set     
            
            
    
def helper_function(widget, color):
    """ Allows color change

    Args:
        widget (Qwidget): Target widget
        color (str): colour code
    """
    widget.setStyleSheet("background-color: {}".format(color.name()))
    
def apply_color_animation(widget, start_color, end_color, duration=1000, loops=1):
    """ Function to indicate what to do via colors

    Args:
        widget (QWidget): target widget
        start_color (str): initial color
        end_color (str): end color, usually original one
        duration (int, optional): transition duration. Defaults to 1000.
        loops (int, optional): number of transitions. Defaults to 1.
    """
    anim = QtCore.QVariantAnimation(
        widget,
        duration=duration,
        startValue=start_color,
        endValue=end_color,
        loopCount=loops,
    )
    anim.valueChanged.connect(functools.partial(helper_function, widget))
    anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)      

        

        
        
          
             
        

                
    
    
    
        

        

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = Main_window()
    
    ui.show()

    sys.exit(app.exec_())
        
       
        