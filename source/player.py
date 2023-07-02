import variables
import pygame
from pygame.sprite import Sprite
import math
import random

class Player(Sprite):
	def __init__(self, playerID, speed, player_sprite_path, planet_radius, planet_center):
		super().__init__()
		self.in_spaceship = None
		self.original_sprite = pygame.image.load(player_sprite_path) # Load the spaceship sprite
		self.original_sprite_scaled = pygame.transform.scale(self.original_sprite, (variables.player_assets_size[playerID]["x"],variables.player_assets_size[playerID]["y"]))
		self.image = self.original_sprite_scaled
		self.rect = self.image.get_rect()
		self.radius = max(self.rect.width // 2, self.rect.height // 2) # radius for collision detection
		self.speed = speed
		# Walking Logic
		self.planet_radius = planet_radius
		self.planet_center = planet_center  # A tuple (x, y)
		self.angle = random.uniform(0, 2*math.pi)  # Initial angle - random between 0 and 2π
		self.previous_angle = self.angle
		self.is_flipped = False  # Add variable to keep track of sprite's direction
		# Calculate initial x and y based on the angle
		self.x, self.y = self.calculate_position(self.angle)
		self.rect.center = (self.x, self.y)

	def respawn(self):
		# Set angle and position to initial state
		self.angle = random.uniform(0, 2*math.pi)  # Initial angle - random between 0 and 2π
		self.x, self.y = self.calculate_position(self.angle)  # Calculate position based on the angle
		self.rect.center = (self.x, self.y)  # Move the player to the new position

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

	def enter_spaceship(self, spaceship, playerID):
		self.in_spaceship = spaceship
		spaceship.controlled = True
		spaceship.playerID = playerID

	def leave_spaceship(self):
		if self.in_spaceship is not None:
			self.in_spaceship.controlled = False
			self.in_spaceship.playerID = None
			self.in_spaceship.reposition()  # Make the spaceship respawn
			self.respawn()  # Make the player respawn
			self.in_spaceship = None
		

	def update(self, playerID):
		# Only accept control input if the player is not in a spaceship
		if self.in_spaceship is None:
			keys = pygame.key.get_pressed()
			if keys[variables.player_controls[playerID]["Move"]["Left"]]:  # Move Left
				self.move_left()
			if keys[variables.player_controls[playerID]["Move"]["Right"]]:  # Move Right
				self.move_right()

		# Update player's x and y based on new angle
		self.x, self.y = self.calculate_position(self.angle)
		self.rect.center = (self.x, self.y)

		# Flip sprite if necessary
		if self.is_flipped:  # Player moved right
			self.image = pygame.transform.flip(self.original_sprite_scaled, True, False)
		else:  # Player moved left or no movement
			self.image = pygame.transform.flip(self.original_sprite_scaled, False, False)

		# Rotate the sprite so its feet are always facing toward the planet
		rotation_angle = math.degrees(-self.angle) + 270  # Convert from radians to degrees and negate, add 90 if sprite initially points right
		self.image = pygame.transform.rotate(self.image, rotation_angle)

		# Update previous_angle for the next frame
		self.previous_angle = self.angle


	def render(self, window):
		window.blit(self.image, (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2))