import variables
import pygame
from pygame.sprite import Sprite
import math
import random

class Player(Sprite):
	def __init__(self, playerID, speed, player_sprite_path, planet_radius, planet_center):
		super().__init__()
		self.original_sprite = pygame.image.load(player_sprite_path) # Load the spaceship sprite
		self.original_sprite_scaled = pygame.transform.scale(self.original_sprite, (variables.player_assets_size[playerID]["x"],variables.player_assets_size[playerID]["y"]))
		self.image = self.original_sprite_scaled.copy()
		self.rect = self.image.get_rect()
		self.speed = speed
		# Walking Logic
		self.planet_radius = planet_radius
		self.planet_center = planet_center  # A tuple (x, y)
		self.angle = random.uniform(0, 2*math.pi)  # Initial angle - random between 0 and 2π
		self.previous_angle = self.angle
		self.is_flipped = False  # Add variable to keep track of sprite's direction
		# Calculate initial x and y based on the angle
		self.x, self.y = self.calculate_position(self.angle)

	def calculate_position(self, angle):
		x = self.planet_center[0] + self.planet_radius * math.cos(angle)
		y = self.planet_center[1] + self.planet_radius * math.sin(angle)
		return x, y

	def move_left(self):
		self.angle -= self.speed / self.planet_radius
		self.is_flipped = False
		

	def move_right(self):
		self.angle += self.speed / self.planet_radius
		self.is_flipped = True
		

	def update(self, playerID):
		keys = pygame.key.get_pressed()
		if keys[variables.player_controls[playerID]["Move"]["Left"]]:  # Move Left
			self.move_left()
		if keys[variables.player_controls[playerID]["Move"]["Right"]]:  # Move Right
			self.move_right()

		# Update player's x and y based on new angle
		self.x, self.y = self.calculate_position(self.angle)

		# Flip sprite if necessary
		if self.is_flipped:  # Player moved right
			self.image = pygame.transform.flip(self.original_sprite_scaled, True, False)
		else:  # Player moved left or no movement
			self.image = pygame.transform.flip(self.original_sprite_scaled, False, False)

		# Rotate the sprite so its feet are always facing toward the planet
		rotation_angle = math.degrees(-self.angle) + 270  # Convert from radians to degrees and negate, add 90 if sprite initially points right
		self.image = pygame.transform.rotate(self.image, rotation_angle)
		# self.image = pygame.transform.scale(rotated_sprite, self.scale)

		# Update previous_angle for the next frame
		self.previous_angle = self.angle


	def render(self, window):
		window.blit(self.image, (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2))