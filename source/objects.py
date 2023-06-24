import pygame
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

class Asteroid:
	def __init__(self, sprite ,screen_center_x, screen_center_y):
		self.sprite = pygame.transform.scale(sprite, (128, 128))
		self.spiral_generator = spiral(screen_center_x, screen_center_y)
		self.x, self.y = next(self.spiral_generator)
		self.half_width = self.sprite.get_width() // 2
		self.half_height = self.sprite.get_height() // 2

	def update(self):
		try:
			self.x, self.y = next(self.spiral_generator)
		except StopIteration:
			# fix the position of the planet if the spiral generator is empty
			pass
	
	def render(self, screen):
		# Draw the object on the screen, adjust the position to center the image
		screen.blit(self.sprite, (self.x - self.half_width, self.y - self.half_height)) 


class Planet:
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.sprite = pygame.transform.scale(sprite, (256, 256))
        self.half_width = self.sprite.get_width() // 2
        self.half_height = self.sprite.get_height() // 2
        self.rotation_angle = 0

    def update(self):
        # Update the rotation angle
        self.rotation_angle += 0.1  # Adjust the rotation speed as needed

    def render(self, screen):
        # Rotate the sprite image
        rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation_angle)
        
        # Get the updated dimensions of the rotated sprite
        rotated_rect = rotated_sprite.get_rect()
        rotated_width = rotated_rect.width
        rotated_height = rotated_rect.height
        
        # Calculate the position to render the rotated sprite
        render_x = self.x - rotated_width // 2
        render_y = self.y - rotated_height // 2
        
        # Draw the rotated sprite on the screen
        screen.blit(rotated_sprite, (render_x, render_y))
		

class Meteor:
    def __init__(self, sprite, screen_width, screen_height, planet_x, planet_y):
        self.sprite = pygame.transform.scale(sprite, (32, 32))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.planet_x = planet_x
        self.planet_y = planet_y

        # Randomly determine the spawn position outside the screen
        spawn_side = random.choice(["top", "bottom", "left", "right"])
        if spawn_side == "top":
            self.x = random.randint(0, self.screen_width)
            self.y = -50
        elif spawn_side == "bottom":
            self.x = random.randint(0, self.screen_width)
            self.y = self.screen_height + 50
        elif spawn_side == "left":
            self.x = -50
            self.y = random.randint(0, self.screen_height)
        elif spawn_side == "right":
            self.x = self.screen_width + 50
            self.y = random.randint(0, self.screen_height)

        # Calculate the direction towards the planet
        direction_x = self.planet_x - self.x
        direction_y = self.planet_y - self.y
        length = math.sqrt(direction_x ** 2 + direction_y ** 2)
        self.direction_x = direction_x / length
        self.direction_y = direction_y / length

    def update(self, speed=1):
        # Update the position based on the direction and speed
        self.x += self.direction_x * speed
        self.y += self.direction_y * speed

        # Check if the meteor is off the screen
        if (
            self.x < -50
            or self.x > self.screen_width + 50
            or self.y < -50
            or self.y > self.screen_height + 50
        ):
            # Respawn the meteor outside the screen
            spawn_side = random.choice(["top", "bottom", "left", "right"])
            if spawn_side == "top":
                self.x = random.randint(0, self.screen_width)
                self.y = -50
            elif spawn_side == "bottom":
                self.x = random.randint(0, self.screen_width)
                self.y = self.screen_height + 50
            elif spawn_side == "left":
                self.x = -50
                self.y = random.randint(0, self.screen_height)
            elif spawn_side == "right":
                self.x = self.screen_width + 50
                self.y = random.randint(0, self.screen_height)

    def render(self, screen):
        # Draw the meteor on the screen
        screen.blit(self.sprite, (self.x, self.y))

