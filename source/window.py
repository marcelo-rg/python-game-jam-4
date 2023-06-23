# window.py
import pygame

class Window:
	def __init__(self, width=800, height=600):
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Pygame Window")
		self.screen.fill((0, 0, 0))  # Fill the screen with a solid color
		pygame.display.flip()  # Update the display after filling it
