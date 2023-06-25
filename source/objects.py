import pygame
from pygame.sprite import Sprite
import math
import random


def spiral(center_x, center_y, radius= 400, speed= 0.005, decay_rate=0.005):
	angle = 0
	while True:
		x = center_x + (radius * math.cos(angle))
		y = center_y + (radius * math.sin(angle))
		
		# Update the angle based on the speed
		angle += speed
		
		# Decrease the radius using the decay_rate
		radius -= decay_rate

		if radius < 0:
			break
		
		yield x, y

class Asteroid(Sprite):
	def __init__(self, sprite ,screen_center_x, screen_center_y):
			super().__init__()
			self.image = pygame.transform.scale(sprite, (128, 128))  # rename sprite to image, as per convention
			self.rect = self.image.get_rect()  
			self.spiral_generator = spiral(screen_center_x, screen_center_y)
			self.rect.center = next(self.spiral_generator)  

	def update(self):
		try:
			self.rect.center = next(self.spiral_generator)
		except StopIteration:
			# fix the position of the planet if the spiral generator is empty
			pass
	
	def render(self, screen):
		screen.blit(self.image, self.rect)  # use rect instead of self.x, self.y


class Planet(Sprite):
	def __init__(self, sprite, x, y):
		super().__init__()
		self.image = pygame.transform.scale(sprite, (256, 256))
		self.rect = self.image.get_rect(center=(x, y))
		self.rotation_angle = 0

	def update(self):
		# Update the rotation angle
		self.rotation_angle += 0.1  # Adjust the rotation speed as needed

	def render(self, screen):
		rotated_sprite = pygame.transform.rotate(self.image, self.rotation_angle)
		rotated_rect = rotated_sprite.get_rect(center=self.rect.center)  # rotate around center
		screen.blit(rotated_sprite, rotated_rect)  # blit at rect's location

		

class Meteor(Sprite):
	def __init__(self, sprite, screen_width, screen_height, planet_x, planet_y):
		super().__init__()
		self.image = pygame.transform.scale(sprite, (32, 32))
		self.rect = self.image.get_rect()
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.planet_x = planet_x
		self.planet_y = planet_y


		# Randomly determine the spawn position outside the screen
		spawn_side = random.choice(["top", "bottom", "left", "right"])
		if spawn_side == "top":
			self.rect.x = random.randint(0, self.screen_width)
			self.rect.y = -50
		elif spawn_side == "bottom":
			self.rect.x = random.randint(0, self.screen_width)
			self.rect.y = self.screen_height + 50
		elif spawn_side == "left":
			self.rect.x = -50
			self.rect.y = random.randint(0, self.screen_height)
		elif spawn_side == "right":
			self.rect.x = self.screen_width + 50
			self.rect.y = random.randint(0, self.screen_height)

		# Calculate the direction towards the planet
		direction_x = self.planet_x - self.rect.x
		direction_y = self.planet_y - self.rect.y
		length = math.sqrt(direction_x ** 2 + direction_y ** 2)
		self.direction_x = direction_x / length
		self.direction_y = direction_y / length

	def update(self, speed=1):
		# Update the position based on the direction and speed
		self.rect.x += self.direction_x * speed
		self.rect.y += self.direction_y * speed

		# Check if the meteor is off the screen
		if (
			self.rect.x < -50
			or self.rect.x > self.screen_width + 50
			or self.rect.y < -50
			or self.rect.y > self.screen_height + 50
		):
			# Respawn the meteor outside the screen
			spawn_side = random.choice(["top", "bottom", "left", "right"])
			if spawn_side == "top":
				self.rect.x = random.randint(0, self.screen_width)
				self.rect.y = -50
			elif spawn_side == "bottom":
				self.rect.x = random.randint(0, self.screen_width)
				self.rect.y = self.screen_height + 50
			elif spawn_side == "left":
				self.rect.x = -50
				self.rect.y = random.randint(0, self.screen_height)
			elif spawn_side == "right":
				self.rect.x = self.screen_width + 50
				self.rect.y = random.randint(0, self.screen_height)
				
			# Calculate the direction towards the planet
			direction_x = self.planet_x - self.rect.x
			direction_y = self.planet_y - self.rect.y
			length = math.sqrt(direction_x ** 2 + direction_y ** 2)
			self.direction_x = direction_x / length
			self.direction_y = direction_y / length

	def render(self, screen):
		# Draw the meteor on the screen
		screen.blit(self.image, self.rect)

