import pygame
from pygame.sprite import Sprite
import math
import random
import variables

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
	def __init__(self, level, spaceship_number, speed, sprite_path, screen_width, screen_height, sound_manager, planet_radius):
		super().__init__()
		self.planet_radius = planet_radius
		self.level = level
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.spaceship_number = spaceship_number
		self.original_sprite = pygame.image.load(sprite_path) # Load the original spaceship sprite
		self.scale = (variables.spaceship_sprite_size["no_upgrade"][spaceship_number][0], 
					  variables.spaceship_sprite_size["no_upgrade"][spaceship_number][1])
		self.original_sprite_scaled = pygame.transform.scale(self.original_sprite, self.scale) # Scale the sprite
		self.image = pygame.transform.scale(self.original_sprite, self.scale) # Scale the sprite
		self.rect = self.image.get_rect()
		self.radius = max(self.rect.width // 2, self.rect.height // 2) # radius for collision detection
		# self.x = variables.spaceship_positions[level][spaceship_number-1][0]
		# self.y = variables.spaceship_positions[level][spaceship_number-1][1]
		self.initial_angle = variables.spaceship_position_angles[level][spaceship_number-1]
		self.reposition()
		self.rect.center = (self.x, self.y)
		self.speed = speed
		self.angle = self.initial_angle
		self.rot_speed = variables.spaceship_rotation_speed


		self.bullets = []  # List to store bullets
		self.shoot_cooldown = 0  # Cool down timer for shooting
		self.shoot_delay = variables.bullet_cooldown  # Delay between shots
		self.sound_manager = sound_manager

	def reposition(self):
		"""Reposition the spaceship to its original location in case of collision."""
		# Load the original position from variables
		# self.x = variables.spaceship_positions[self.level][self.spaceship_number-1][0]
		# self.y = variables.spaceship_positions[self.level][self.spaceship_number-1][1]
		platet_center_x, platet_center_y = (self.screen_width//2, self.screen_height//2)
		self.x = platet_center_x + (self.planet_radius +self.radius)* math.cos(self.initial_angle)
		self.y = platet_center_y + (self.planet_radius +self.radius)* math.sin(self.initial_angle)
		self.angle = self.initial_angle
		self.image = pygame.transform.rotate(self.original_sprite_scaled, self.initial_angle)

		# Apply the position to the spaceship rect
		self.rect.center = (self.x, self.y)

	def shoot(self):
		# Compute the offset position of the bullet
		half_height = self.rect.height / 2
		adjusted_angle = math.radians(-self.angle - 90)  # Convert angle to radians and adjust by -90 degrees
		offset_x = half_height * math.cos(adjusted_angle)
		offset_y = half_height * math.sin(adjusted_angle)

		# Compute the bullet's initial position
		bullet_x = self.x + offset_x
		bullet_y = self.y + offset_y

		# Create a new bullet and add it to the bullets list
		bullet = Bullet(bullet_x, bullet_y, self.angle, variables.bullet_speed, variables.bullet_sprite_path, variables.bullet_sprite_size, self.screen_width, self.screen_height)
		self.bullets.append(bullet)


	def rotate_left(self):
		self.angle += self.rot_speed
		self.image = pygame.transform.rotate(self.original_sprite_scaled, self.angle)
		self.rect = self.image.get_rect(center=self.rect.center)

	def rotate_right(self):
		self.angle -= self.rot_speed
		self.image = pygame.transform.rotate(self.original_sprite_scaled, self.angle)
		self.rect = self.image.get_rect(center=self.rect.center)

	def move_forward(self):
		self.move(self.speed)

	def move_backward(self):
		self.move(-self.speed)

	def move(self, distance):
		adjusted_angle = -self.angle - 90
		radians = math.radians(adjusted_angle)
		new_x = self.x + distance * math.cos(radians)
		new_y = self.y + distance * math.sin(radians)

		# Adjust the new x and y positions to ensure the spaceship does not go offscreen
		new_x = max(min(new_x, self.screen_width - self.rect.width / 2), self.rect.width / 2)
		new_y = max(min(new_y, self.screen_height - self.rect.height / 2), self.rect.height / 2)

		# Calculate the distance to the center of the screen (where the planet is)
		center_x = self.screen_width / 2
		center_y = self.screen_height / 2
		dist_to_center = ((new_x - center_x)**2 + (new_y - center_y)**2)**0.5  # Pythagorean theorem

		# Check if the spaceship would go inside the planet
		if dist_to_center < self.planet_radius + self.radius:  # I'm assuming the planet_radius is accessible from the variables module
			return  # If it would, block the movement

		# If it wouldn't, apply the movement
		self.x = new_x
		self.y = new_y

		self.rect.center = (self.x, self.y)

	def cleanup_bullets(self):
		"""Removes 'dead' bullets from the bullets list."""
		self.bullets = [bullet for bullet in self.bullets if bullet.is_alive]

	def update(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]: # A key
			self.rotate_left()
		if keys[pygame.K_d]: # D key
			self.rotate_right()
		if keys[pygame.K_w]: # W key
			self.move_forward()
		if keys[pygame.K_s]: # S key
			self.move_backward()
		if keys[variables.player_controls['Player1']['Fire']['Use']] and self.shoot_cooldown <= 0: # change 'Player1' to a player id variable
			self.shoot()
			self.sound_manager.playSoundEffect('shooting')
			self.shoot_cooldown = self.shoot_delay # Reset the cooldown 
		
		# Reduce the cooldown over time
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1

		# Update the position of all bullets
		for bullet in self.bullets:
			bullet.update()

		# Remove dead bullets
		self.cleanup_bullets()

	def render(self, window):
		window.blit(self.image, self.rect)
		for bullet in self.bullets:
			bullet.render(window)


class Bullet(Sprite):
	def __init__(self, x, y, angle, speed, bullet_sprite_path, bullet_scale, screen_width, screen_height):
			super().__init__()
			self.x = x
			self.y = y
			self.angle = -angle -90
			self.speed = speed
			self.is_alive = True  # Bullet is initially alive
			self.screen_width = screen_width
			self.screen_height = screen_height

			self.original_sprite = pygame.image.load(bullet_sprite_path)
			self.original_sprite_scaled = pygame.transform.scale(self.original_sprite, bullet_scale)

			# Rotate the bullet sprite to match the spaceship's angle
			self.image = pygame.transform.rotate(self.original_sprite_scaled, -self.angle)

			self.rect = self.image.get_rect(center=(self.x, self.y))
			self.radius = max(self.rect.width // 2, self.rect.height // 2) # radius for collision detection

	def remove(self):
		"""Mark the bullet as 'dead' so it can be removed."""
		self.is_alive = False

	def update(self):
		# Calculate the new position of the bullet
		self.x += self.speed * math.cos(math.radians(self.angle))
		self.y += self.speed * math.sin(math.radians(self.angle))
		self.rect.center = (self.x, self.y)

		# Check if the bullet has gone off-screen
		if self.x < 0 or self.x > self.screen_width or self.y < 0 or self.y > self.screen_height:
			self.remove()

	def render(self, window):
		window.blit(self.image, self.rect)

