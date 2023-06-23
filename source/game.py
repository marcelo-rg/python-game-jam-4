import pygame
import window as win

class Game:
	def __init__(self):
		pygame.init()
		self.window = None

	def run(self):
		self.window = win.Window()

		# Game loop
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			# Fill the screen with a solid color
			self.window.screen.fill((0, 0, 0))

			# Update the full display Surface to the screen
			pygame.display.flip()

		# Once we have exited the main program loop we can stop the game engine:
		pygame.quit()

# Run the game
game = Game()
game.run()