# Conway`s Game of Life

Conway's Game of Life using PyQt5 library


## Description

This app is an installment of the simulation known as "Game of Life" by Conway. Uses PyQt5 as its main library. 

As Pqt5 is not intended for this kind of uses it creates som issues that requiered some compromises. The main one was related with the cells. The most obvious solution to this problem is creating and destroying cells as part of the simulation. However PyQt5 generated some problems with this approach, so it was opted to create all cells once as QLabels and make them change status/color from dead to alive. This limits the number of cells available. The issue with the main game loop, thing that is obviously not implemented in PyQt5 was solved simply by using a timer and an UI update function.

### Dependencies

* PyQt5
* sys
* functools
  
## Running the simulation

Run game.py. Upon the app starting a blanck board will appear. Clicking on it will change the correspondent cell status from dead to alive and backwards. To start the simulation click "Start Simulation".

![game running](https://github.com/user-attachments/assets/26a2dbde-7514-4a0e-93d1-0a9c2a94a16e)

To stop the simulation press "Stop Simulation". There is also an option to restart the whole game.




## Author:

Leonardo Mario Mazzeo
leomazzeo@gmail.com
