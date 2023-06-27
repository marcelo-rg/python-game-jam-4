import variables
import pygame
from pygame.sprite import Sprite
import math
import random

class Player(Sprite):
	def __init__(self, playerID, speed, player_sprite_path, planet_radius, planet_center):
		super().__init__()
		self.sprite = pygame.image.load(player_sprite_path) # Load the spaceship sprite
		self.image = pygame.transform.scale(self.sprite, (variables.player_assets_size[playerID]["x"],variables.player_assets_size[playerID]["y"]))
		self.rect = self.image.get_rect()
		self.speed = speed
		# Walking Logic
		self.radius = planet_radius
		self.planet_center = planet_center  # A tuple (x, y)
		self.angle = random.uniform(0, 2*math.pi)  # Initial angle - random between 0 and 2π
		# Calculate initial x and y based on the angle
		self.x = self.planet_center[0] + self.radius * math.cos(self.angle)
		self.y = self.planet_center[1] + self.radius * math.sin(self.angle)

	def move_left(self):
		#self.x -= self.speed
		self.angle -= self.speed / self.radius

	def move_right(self):
		#self.x += self.speed
		self.angle += self.speed / self.radius

	def update(self,playerID):
		keys = pygame.key.get_pressed()
		if keys[variables.player_controls[playerID]["Move"]["Left"]]:  # Move Left
			self.move_left()
		if keys[variables.player_controls[playerID]["Move"]["Right"]]:  # Move Right
			self.move_right()

		# Update player's x and y based on new angle
		self.x = self.planet_center[0] + self.radius * math.cos(self.angle)
		self.y = self.planet_center[1] + self.radius * math.sin(self.angle)

		# Rotate the sprite so its feet are always facing toward the planet
		self.image = pygame.transform.rotate(self.sprite, math.degrees(self.angle) - 180)

	def render(self, window):
		# The sprite's position is its center, adjust for this
		window.blit(self.image, (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2))