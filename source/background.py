import pygame
from pygame.locals import *
import variables

class Background:
	def __init__(self, screen):
		self.screen = screen

	def set_background(self, image_path):
		# Blit background image onto display
		self.width = variables.screen_width
		self.height = variables.screen_height
		self.background_image = pygame.image.load(image_path)
		self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
		self.screen.blit(self.background_image, (0, 0))

