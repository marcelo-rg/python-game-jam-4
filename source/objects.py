import pygame
from pygame.sprite import Sprite
import math
import random
import variables
from player import Player

def spiral(center_x, center_y, radius= variables.spiral_radius, speed= variables.spiral_speed, decay_rate=variables.spiral_decay_rate):
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

			self.image = pygame.transform.scale(sprite, (variables.asteroid_sprite_size, variables.asteroid_sprite_size))
			self.rect = self.image.get_rect()  
			self.spiral_generator = spiral(screen_center_x, screen_center_y)
			self.rect.center = next(self.spiral_generator)  
			self.radius = min(self.rect.width // 2, self.rect.height // 2) # radius for collision detection


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

		self.original_image = pygame.transform.scale(sprite, (variables.planet_sprite_size, variables.planet_sprite_size))  # Save the original image for rotating
		self.image = self.original_image.copy()  # Create a copy to modify with rotation
		self.rect = self.image.get_rect(center=(x, y))
		self.rotation_angle = 0
		self.radius = max(self.rect.width // 2, self.rect.height // 2) # radius for collision detection

	def update(self):
		# Update the rotation angle
		self.rotation_angle += 0.1  # Adjust the rotation speed as needed

		# Rotate the original image without modifying it and get a new rect
		self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
		self.rect = self.image.get_rect(center=self.rect.center)  # rotate around center

	def render(self, screen):
		screen.blit(self.image, self.rect)  # blit at rect's location
		

class Meteor(Sprite):
	def __init__(self, sprite, screen_width, screen_height, planet_x, planet_y):
		super().__init__()
		self.original_image = pygame.transform.scale(sprite, (variables.meteor_sprite_size, variables.meteor_sprite_size))
		self.image = self.original_image.copy()  # Create a copy to modify with rotation
		self.rect = self.image.get_rect()
		self.rotation_angle = 0  

		self.image =  pygame.transform.scale(sprite, (variables.meteor_sprite_size, variables.meteor_sprite_size))
		self.rect = self.image.get_rect()

		self.screen_width = screen_width
		self.screen_height = screen_height
		self.planet_x = planet_x
		self.planet_y = planet_y
		self.radius = max(self.rect.width // 2, self.rect.height // 2) # radius for collision detection


		# Randomly determine the spawn position outside the screen
		self.respawn()

		# Calculate the direction towards the planet
		self.gravity = 0.1  # Adjust the gravity factor as needed

		self.calculate_direction()

		# Add two new attributes for the floating point position
		self.pos_x = float(self.rect.centerx)
		self.pos_y = float(self.rect.centery)

	def calculate_direction(self):
		# Calculate the direction towards the planet
		direction_x = self.planet_x - self.pos_x
		direction_y = self.planet_y - self.pos_y
		length = math.sqrt(direction_x ** 2 + direction_y ** 2)
		self.velocity_x = (direction_x / length)
		self.velocity_y = (direction_y / length)


	def respawn(self):
		spawn_side = random.choice(["top", "bottom", "left", "right"])
		if spawn_side == "top":
			self.pos_x = random.uniform(0, self.screen_width)
			self.pos_y = -50.0
		elif spawn_side == "bottom":
			self.pos_x = random.uniform(0, self.screen_width)
			self.pos_y = self.screen_height + 50.0
		elif spawn_side == "left":
			self.pos_x = -50.0
			self.pos_y = random.uniform(0, self.screen_height)
		elif spawn_side == "right":
			self.pos_x = self.screen_width + 50.0
			self.pos_y = random.uniform(0, self.screen_height)

		# Update rect's center
		self.rect.centerx = round(self.pos_x)
		self.rect.centery = round(self.pos_y)

		self.calculate_direction()


	def update(self, speed=1.5):
		# Update the rotation angle
		self.rotation_angle += 0.5  # Adjust the rotation speed as needed

		# Rotate the original image without modifying it
		self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)

		# Update the position based on the direction, speed and gravity
		self.pos_x += self.velocity_x * speed
		self.pos_y += self.velocity_y * speed

		# Convert floating point position values to integer for rect
		self.rect.centerx = round(self.pos_x)
		self.rect.centery = round(self.pos_y)

		# Check if the meteor is off the screen and respawn if it is
		if (
			self.rect.centerx < -50
			or self.rect.centerx > self.screen_width + 50
			or self.rect.centery < -50
			or self.rect.centery > self.screen_height + 50
			):
			self.respawn()  # Call the respawn method

	def render(self, screen):
		# Draw the meteor on the screen
		screen.blit(self.image, self.rect)

class Spaceship(Sprite):
	def __init__(self, level, spaceship_number, speed, sprite_path):
		super().__init__()
		self.sprite = pygame.image.load(sprite_path) # Load the spaceship sprite
		self.image = pygame.transform.scale(self.sprite, (variables.spaceship_sprite_size["no_upgrade"][spaceship_number][0], 
						    variables.spaceship_sprite_size["no_upgrade"][spaceship_number][1]))
		self.rect = self.image.get_rect()
		self.x = variables.spaceship_positions[level][spaceship_number-1][0]
		self.y = variables.spaceship_positions[level][spaceship_number-1][1]
		self.speed = speed

	def move_left(self):
		self.x -= self.speed

	def move_right(self):
		self.x += self.speed

	def move_up(self):
		self.y -= self.speed

	def move_down(self):
		self.y += self.speed

#	def update(self):
#		keys = pygame.key.get_pressed()
#		if keys[pygame.K_LEFT]: # Left arrow key
#			self.move_left()
#		if keys[pygame.K_RIGHT]: # Right arrow key
#			self.move_right()
#		if keys[pygame.K_UP]: # Up arrow key
#			self.move_up()
#		if keys[pygame.K_DOWN]: # Down arrow key
#			self.move_down()
	
	def render(self, window):
		window.blit(self.image, (self.x, self.y))