######################################################
### Conway's Game of life                         ####
### Author: Leonardo Mario Mazzeo                 ####
######################################################


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

grid = [[False for y in range(NUMBER_OF_ROW)] for x in range(NUMBER_OF_COL)]    # Cells get their state from this list of list. False is default indicating all cells are dead


class Cell(QLabel):
    """ Cell object. One is created for every position on the board/habitat.
    Method for interaction is included in the object

    
    """
    
    
    def __init__(self, reference_frame, xpos, ypos):
        """Cell object. One is created for every position on the board/habitat.
    Method for interaction is included in the object 
        Args:
            reference_frame (Qframe): Board/habitat
            xpos (int): x position
            ypos (int): y position
        """
        
        changestate = pyqtSignal(bool)
        
        QLabel.__init__(self, reference_frame)
        
        self.setObjectName(str(xpos)+","+str(ypos))     # defined to track the object by its relative position in the grid
        self.setGeometry(QtCore.QRect(xpos*CELL_SIZE,ypos*CELL_SIZE,CELL_SIZE,CELL_SIZE))   #shape of the cell
        self.alive = False       # cell state indicator. Used to change the color of the Qlabel
        
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))    # change cursor over the cell. In practice changes the cursor over the board/habitat
    
        self.setMouseTracking(True)     # activates mouse tracking method for the cell
        
            
    def mousePressEvent(self, QMouseEvent):
        """ Mouse interaction method. Changes the state of the clicked cell from alive to dead otherwise. 

        """
        super(Cell, self).mousePressEvent(QMouseEvent) # mouse event detector
        
        # get the relative position from objectname method in QLabel and changes the state in the grid 
        grid[int(self.objectName()[:self.objectName().find(",")])][int(self.objectName()[self.objectName().find(",")+1:])] = not grid[int(self.objectName()[:self.objectName().find(",")])][int(self.objectName()[self.objectName().find(",")+1:])]
        
        self.alive = not self.alive   # change the state in alive indicator
        self.alive_or_not()   # change color of cell via method
    
    def initial_setup(self):
        """ Defines the initial state while the simulation is stopped
        """
        if self.alive: self.setStyleSheet("background-color: white")
        else: self.setStyleSheet("background-color: black")
    
    def alive_or_not(self):
        """ Method to change the color form alive to dead
        """
        if self.alive: 
            apply_color_animation(self, QtGui.QColor("black"), QtGui.QColor("white"), duration=200)
            
        else: 
            apply_color_animation(self, QtGui.QColor("white"), QtGui.QColor("black"), duration=200)
            
   
        
class Main_window(QMainWindow):
    def __init__(self):
        """ Main function
        """
        global grid
        super(Main_window, self).__init__()
        
        # Main window
        self.setObjectName("MainWindow")   
        self.resize(1000, 900)
        self.setWindowTitle("MainWindow")
        self.setStyleSheet("background-color: dimgray")
        self.setWindowTitle("Game of life")
        
        # Board/habitat
        self.game_frame = QFrame(self)   
        self.game_frame.resize(900,900)
        self.game_frame.setStyleSheet("background-color: black")
        
        # Button to start/stop simulation -> green indicates ready to start, red the simulation is in process and can be stopped
        self.evolve_button = QPushButton(self)
        self.evolve_button.setShortcut("Space")
        self.evolve_button.setGeometry(QtCore.QRect(905,10,90,50))
        self.evolve_button.released.connect(lambda: self.launch())
        self.evolve_button.setStyleSheet("background-color: darkgreen")
        self.evolve_button.setText("Start Simulation")
        
        # Button to clear the habitat and restart the simulation killing all cells
        self.clear_button = QPushButton(self)
        self.clear_button.setText("Clear all cells")
        self.clear_button.setStyleSheet("background-color: gold")
        self.clear_button.setGeometry(QtCore.QRect(905,80,90,50))
        self.clear_button.clicked.connect(lambda: self.cleaner())
        
        # Cycles counter. Indicates the number of tiems the games loops. It is restarted once the habitat is cleared via clear_button
        self.cycle_counter = 0
        
        self.cycles = QLabel(self)
        self.cycles.setText("cycles: "+str(self.cycle_counter))
        self.cycles.setGeometry(905, 140, 90, 40)
        self.cycles.setStyleSheet("color: red")
        
        # Timer control PyQT5 object. Used to loop and prevent freezing and instant solutions
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.life)
        
        # Calling the initial setup the 
        self.cell_creator()
        
        # Boolean to indicate game situation, if True -> evolve_button = green 
        self.isalive = True 
        
        
    def cell_creator(self):
        
        """ Populates the board/habitat at start with dead cells
        """
        
        for x in range(NUMBER_OF_COL):
            for y in range(NUMBER_OF_ROW):
                Cell(self.game_frame, x, y)
    
                    
    def cell_assigner(self, tochange): # Needed to signal the change of state to cells
        """ Detects the cells that change status. Loops thorught all cells and select the ones that change their state. 

        Args:
            tochange (set): cordinates of the cells that must change state
        """
        
        for uniquecell in tochange: # get the cells to change status
            one_cell = self.game_frame.findChild(Cell, uniquecell) # choose the cell
            one_cell.alive = grid[int(uniquecell[:uniquecell.find(",")])][int(uniquecell[uniquecell.find(",")+1:])] # get the new state
            one_cell.alive_or_not() # apply the new state
     
    def life(self):
        """ Launches the UI to the functions conrolling the game
        """
        changed = growth() # Launches the function that creates the game
        self.cell_assigner(changed) # send signals to the UI
        self.cycle_counter += 1 # cycles counter
        self.cycles.setText("cycles: "+str(self.cycle_counter)) # inform cycles
        
   
    def launch(self):
        """ Starts and stops the game
        """
           
        if self.isalive:
            self.isalive = False
            self.timer.start() # Start timer / launch simulation loop
            self.evolve_button.setText("Stop Simulation")
            self.evolve_button.setStyleSheet("background-color: darkred")
            
        else: 
            self.isalive = True
            self.timer.stop() # stop timer / stop simulation loop
            self.evolve_button.setText("Start Simulation")
            self.evolve_button.setStyleSheet("background-color: darkgreen")
            
    def cleaner(self):
        """ Cleans the whole board
        """
        self.timer.stop() # stop timer / stop simulation loop
        clear() # clear the whole grid
        for y in range(NUMBER_OF_ROW):
            for x in range(NUMBER_OF_COL):
                one_cell = self.game_frame.findChild(Cell, str(x)+","+str(y))
                one_cell.alive = grid[x][y]
                one_cell.initial_setup() # return the cells to their initial state / dead
        self.cycle_counter = 0 # cycles to cero
        self.cycles.setText("cycles: "+str(self.cycle_counter))
        self.isalive = True # allow to restart the simulation
        self.evolve_button.setText("Start Simulation")
        self.evolve_button.setStyleSheet("background-color: darkgreen")
    
    
 
def clear():
    """Restart the grid
    """
    for col in range(NUMBER_OF_COL):
        for row in range(NUMBER_OF_ROW):
            grid[col][row] = False
          

def neighborhood(posx, posy, habitat):
    """ Generate the list of alive neighbours of a cell

    Args:
        posx (int): x cordinates of the cell
        posy (int): y cordinates of the cell
        habitat (list): list of list forming a grid

    Returns:
        int: number of alive neighbours
    """
    alive_neighbor = 0 # alive cells counter
    
    # define the verticals neighbours
    if posx == 0:   
        ontheleft=posx
    else: ontheleft = posx-1
    if posx == NUMBER_OF_COL-1:
        ontheright = posx+1
    else: ontheright = posx+2
    
    # define the horizontal neighbours
    if posy == 0:
        ontop=posy
    else: ontop = posy-1
    if posy == NUMBER_OF_ROW-1:
        onbottom = posy+1
    else: onbottom = posy+2
    
    # get the alive nighbours
    for x in range(ontheleft,ontheright):
        for y in range(ontop,onbottom):
            if x == posx and y == posy:
                pass
            else: 
                if habitat[x][y]:
                    alive_neighbor += 1
    return alive_neighbor
    
def alive(posx, posy, habitat, habitatoriginal):
    """ Game rules function. Changes the state of individual cell

    Args:
        posx (int): x coordinate of the tested cell
        posy (int): y coordinate of the tested cell
        habitat (list): blanck grid type list
        habitatoriginal (list): previous cycle grid list

    Returns:
        tuple: (indicator to check change of state(str), grid list with the new state of the cell(list))
    """
    status_change_indicator = str # indicates the cell to change state
    near_cells = neighborhood(posx, posy, habitatoriginal)  # get the number of alive neighbours
    
    # rules of the game
    if habitatoriginal[posx][posy]:
        if near_cells < 2 or near_cells > 3: 
            habitat[posx][posy] = False
            status_change_indicator = str(posx)+","+str(posy)
        
        else:
            habitat[posx][posy] = True
            status_change_indicator = ""    
    else: 
        if near_cells == 3: 
            habitat[posx][posy] = True
            status_change_indicator = str(posx)+","+str(posy)
        else:
            habitat[posx][posy] = False
            status_change_indicator = "" 
    return status_change_indicator, habitat

def growth():
    """ Grid updater and signal creator for the UI. Returns a set composed of str indicating the coordinates of the cells that change their state

    Returns:
        set: set of str of coordinates. Only changing cells appear
    """
    
    global grid
    
    previous = grid.copy() # prevent sequential change generating errors
    habitatnew = [[False for y in range(NUMBER_OF_ROW)] for x in range(NUMBER_OF_COL)] # blank grid to load new states
    changed_status = [] # temporal list for cell signals
    for x in range(NUMBER_OF_COL):
        for y in range(NUMBER_OF_ROW):
            new_status, habitatnew = alive(x,y,habitatnew, previous) # apply the rules
            changed_status.append(new_status) # load the signals to the temporal list
    changed_set = set(changed_status) # clear duplicates
    changed_set.remove("") # clear the useless data
    grid = habitatnew # update the grid
    
    return changed_set     
            
            
    
def colour_gradient_function(widget, color):
    """ Allows color change

    Args:
        widget (Qwidget): Target widget
        color (str): colour code
    """
    widget.setStyleSheet("background-color: {}".format(color.name()))
    
def apply_color_animation(widget, start_color, end_color, duration=100, loops=1):
    """ Function get slow colour transitions
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
    anim.valueChanged.connect(functools.partial(colour_gradient_function, widget))
    anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)      

        

        
        
          
             
        

                
    
    
    
        

        

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = Main_window()
    
    ui.show()

    sys.exit(app.exec_())
        
       
        