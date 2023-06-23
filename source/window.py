import pygame

class Window:
	# The constructor
	def __init__(self, width = 800,height=600):
		# Initialize the Pygame
		pygame.init()
		# Set the dimensions of the window
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))

		# Fill the screen with a solid color
		self.screen.fill((0, 0, 0))

	def createGame(self):
		# Game loop
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			# Fill the screen with a solid color
			self.screen.fill((0, 0, 0))

			# Update the full display Surface to the screen
			pygame.display.flip()

		# Once we have exited the main program loop we can stop the game engine:
		pygame.quit()
