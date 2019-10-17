from classes import *
import tkinter as tk

game = Game(10, 10)

game.render()

while True:
    
    game.take_direction()
    position = game.calc_position()
    if (position==np.asarray([None, None])).all():
        break
    game.snake.take_step(position)
    game.render()
    
