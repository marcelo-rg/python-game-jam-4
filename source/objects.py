import pygame
from pygame.sprite import Sprite
import math
import random
import variables

def spiral(center_x, center_y, radius= variables.spiral_radius, base_speed= variables.spiral_speed, decay_rate=variables.spiral_decay_rate, speed_factor=variables.spiral_speed_factor):
	angle = 0
	while True:
		x = center_x + (radius * math.cos(angle))
		y = center_y + (radius * math.sin(angle))

		# Update the angle based on the speed which increases as the asteroid gets closer
		speed = base_speed + speed_factor / max(1, radius)
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


	def update(self, speed):
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
		self.upgraded = False
		self.controlled = False
		self.playerID = None
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
		self.reposition(spaceship_number)
		self.rect.center = (self.x, self.y)
		self.speed = speed
		self.angle = self.initial_angle
		self.rot_speed = variables.spaceship_rotation_speed
		self.repair_cooldown_frames = variables.game_data[variables.current_level]["spaceship_repair_cooldown"]  
		self.repair_frame_counter = 0  # counter to track the number of frames since the repair process started
		# self.repairing = False  # flag to indicate if the spaceship is currently being repaired
		self.hp = variables.game_data[variables.current_level]["spaceship_one_hp"]["max"]

		self.bullets = []  # List to store bullets
		self.shoot_cooldown = 0  # Cool down timer for shooting
		self.shoot_delay = variables.bullet_cooldown  # Delay between shots
		self.sound_manager = sound_manager

	def reset_repair_counter(self):
		self.repair_frame_counter = 0  # reset the frame counter

	def repair(self):
		if self.repair_frame_counter < self.repair_cooldown_frames:
			# Calculate the amount of HP to recover in this frame
			hp_recovery_per_frame = variables.game_data[variables.current_level]["spaceship_one_hp"]["max"] / self.repair_cooldown_frames
			self.hp += hp_recovery_per_frame
			# Make sure the HP doesn't exceed the maximum
			self.hp = min(self.hp, variables.game_data[variables.current_level]["spaceship_one_hp"]["max"])
			self.repair_frame_counter += 1
		else:
			return True  # Repair process is complete
		return False  # Repair process is ongoing
	
	def upgrade(self, new_spaceship_sprite_path):
		"""Upgrades the spaceship sprite and other properties."""
		self.upgraded = True
		# Load the new sprite
		self.original_sprite = pygame.image.load(new_spaceship_sprite_path)
		self.original_sprite_scaled = pygame.transform.scale(self.original_sprite, self.scale)

		if self.spaceship_number == 1:
			# Rotate the scaled original sprite by 180 degrees
			self.original_sprite_scaled = pygame.transform.rotate(self.original_sprite_scaled, 180)
			# Set the image using the current angle
			self.image = pygame.transform.rotate(self.original_sprite_scaled, self.angle)
		else:
			# Set the image using the current angle
			self.image = pygame.transform.rotate(self.original_sprite_scaled, self.angle)




	def reposition(self, spaceship_number):
		"""Reposition the spaceship to its original location in case of collision."""
		# Load the original position from variables
		# self.x = variables.spaceship_positions[self.level][self.spaceship_number-1][0]
		# self.y = variables.spaceship_positions[self.level][self.spaceship_number-1][1]
		planet_center_x, planet_center_y = (self.screen_width//2, self.screen_height//2)

		if (spaceship_number == 1): # this is the green asset spaceship
			self.x = planet_center_x + (self.planet_radius + self.radius) * math.cos(self.initial_angle)
			self.y = planet_center_y + (self.planet_radius + self.radius) * math.sin(self.initial_angle)
			self.angle = self.initial_angle + 180
			self.image = pygame.transform.rotate(self.original_sprite_scaled, self.angle)

			# print(self.initial_angle)
			# # print initial angle in degrees
			# print(math.degrees(self.initial_angle))
			# print(math.degrees(self.angle))
			# exit()
			self.original_sprite_scaled = pygame.transform.rotate(self.original_sprite_scaled, self.angle)
		else:
			# Change these lines to reflect the different initial position and angle for spaceship 2
			self.x = planet_center_x + (self.planet_radius + self.radius) * math.cos(self.initial_angle)
			self.y = planet_center_y + (self.planet_radius + self.radius) * math.sin(self.initial_angle)
			self.angle = self.initial_angle
			self.image = pygame.transform.rotate(self.original_sprite_scaled, self.angle)

		# self.radius = max(self.rect.width // 2, self.rect.height // 2) # radius for collision detection

		# Apply the position to the spaceship rect
		self.rect.center = (self.x, self.y)

	def shoot(self):
		# Compute the offset position of the bullet
		half_height = self.rect.height / 2
		adjusted_angle =-self.angle - 90 # Convert angle to radians and adjust by -90 degrees
		if self.spaceship_number == 1:
			adjusted_angle += 180
		radians = math.radians(adjusted_angle)
		offset_x = half_height * math.cos(radians)
		offset_y = half_height * math.sin(radians)

		# Compute the bullet's initial position
		bullet_x = self.x + offset_x
		bullet_y = self.y + offset_y

		# Create a new bullet and add it to the bullets list
		if self.upgraded:
			asset_path = variables.bullet_sprite_path_upgraded
		else:
			asset_path = variables.bullet_sprite_path

		bullet_angle = self.angle
		if self.spaceship_number == 1:
			bullet_angle += 180
		bullet = Bullet(bullet_x, bullet_y, bullet_angle, variables.bullet_speed, asset_path, variables.bullet_sprite_size, self.screen_width, self.screen_height)
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
		if self.spaceship_number == 1:
			adjusted_angle += 180  # Additional adjustment for the green asset spaceship
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
		if dist_to_center < self.planet_radius + self.radius: 
			return  # If it would, block the movement

		# If it wouldn't, apply the movement
		self.x = new_x
		self.y = new_y

		self.rect.center = (self.x, self.y)

	def cleanup_bullets(self):
		"""Removes 'dead' bullets from the bullets list."""
		self.bullets = [bullet for bullet in self.bullets if bullet.is_alive]

	def update(self):
		# Only accept control input if the spaceship is controlled by the player
		if self.controlled:
			keys = pygame.key.get_pressed()
			if keys[variables.player_controls[self.playerID]["Move"]["Left"]]: # A key
				self.rotate_left()
			if keys[variables.player_controls[self.playerID]["Move"]["Right"]]: # D key
				self.rotate_right()
			if keys[variables.player_controls[self.playerID]["Move"]["Up"]]: # W key
				self.move_forward()
			if keys[variables.player_controls[self.playerID]["Move"]["Down"]]: # S key
				self.move_backward()
			if keys[variables.player_controls[self.playerID]['Fire']['Use']] and self.shoot_cooldown <= 0: 
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

	def upgrade(self, new_bullet_sprite_path):
		"""Upgrades the bullet sprite."""
		# Load the new sprite
		self.original_sprite = pygame.image.load(new_bullet_sprite_path)
		self.original_sprite_scaled = pygame.transform.scale(self.original_sprite, self.original_sprite_scaled.get_size())

		# Rotate the new sprite to match the spaceship's angle
		self.image = pygame.transform.rotate(self.original_sprite_scaled, -self.angle)


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

