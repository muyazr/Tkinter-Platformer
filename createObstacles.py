import tkinter as tk

def fourTileObstacle(canvas, createObstacles, xPosition,level = 1):
    if level == 1:
        position = [xPosition, 610]
    else:
        position = [xPosition, 410]
    
    createObstacles.append([canvas.create_image(position[0], position[1]), canvas.create_rectangle(position[0] - 153, position[1] - 43, position[2] + 67, position[3] - 83), "fourTile"])
