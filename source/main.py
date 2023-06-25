from game import Game
import variables
from mainMenu import *

if __name__ == "__main__":
	# Create a Menu instance and start it
	menu = Menu(variables.screen_width, variables.screen_height, variables.fps)
	menu.start()