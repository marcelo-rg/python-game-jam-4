import pygame
import math


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



# import pygame

# class Asteroid:
#     def __init__(self, x, y, image_path):
#         self.position = pygame.Vector2(x, y)
#         self.sprite = pygame.image.load(image_path)
#         self.sprite = pygame.transform.scale(self.sprite, (128, 128))

#     def update(self, keys_pressed):
#         # Update the position based on user input or game logic
#         if keys_pressed[pygame.K_w]:
#             self.position.y -= 1
#         elif keys_pressed[pygame.K_s]:
#             self.position.y += 1
#         elif keys_pressed[pygame.K_a]:
#             self.position.x -= 1
#         elif keys_pressed[pygame.K_d]:
#             self.position.x += 1

#     def draw(self, screen):
#         # Draw the object on the screen
#         screen.blit(self.sprite, self.position) 



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
		