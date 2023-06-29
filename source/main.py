from game import Game
import variables
import pygame
import sys
from pygame.locals import *
from mainMenu import MainMenu  # Import the MainMenu class

if __name__ == "__main__":
	# Create a Menu instance and start it
	pygame.init()
	menu = MainMenu(variables.fps)
	menu.start()