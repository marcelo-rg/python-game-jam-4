import pygame
import math


def spiral(center_x, center_y, radius, speed):
	angle = 0
	while True:
		x = center_x + (radius * math.cos(angle))
		y = center_y + (radius * math.sin(angle))
		
		# Update the angle based on the speed
		angle += speed
		
		yield x, y


class Planet:
	def __init__(self, sprite ,screen_center_x, screen_center_y, radius, speed):
		self.sprite = pygame.transform.scale(sprite, (128, 128))
		self.spiral_generator = spiral(screen_center_x, screen_center_y, radius, speed)
		self.x, self.y = next(self.spiral_generator)
		self.half_width = self.sprite.get_width() // 2
		self.half_height = self.sprite.get_height() // 2

	def update(self):
		self.x, self.y = next(self.spiral_generator)
	
	def render(self, screen):
		# Draw the object on the screen, adjust the position to center the image
		screen.blit(self.sprite, (self.x - self.half_width, self.y - self.half_height)) 
