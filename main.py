import sys
sys.path.append('./source/')
import variables
import pygame
from pygame.locals import *
from mainMenu import MainMenu  # Import the MainMenu class
from saveGame import SaveGame  # Import the SaveGame class

if __name__ == "__main__":
	# Create a Menu instance and start it
	pygame.init()
	saveObject = SaveGame()
	saveObject.load(variables.player_file)
	menu = MainMenu(variables.fps)
	menu.start()