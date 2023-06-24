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


class Asteroid:
    def __init__(self, sprite ,screen_center_x, screen_center_y, radius, speed):
        self.sprite = pygame.transform.scale(sprite, (128, 128))
        asteroid_rect = self.sprite.get_rect()
        asteroid_x = (screen_center_x - asteroid_rect.width) // 2
        asteroid_y = (screen_center_y - asteroid_rect.height) // 2
        self.spiral_generator = spiral(asteroid_x,asteroid_y, radius, speed)
        self.x, self.y = next(self.spiral_generator)
    
    def update(self):
        self.x, self.y = next(self.spiral_generator)
    
    def render(self, screen):
        # Draw the object on the screen
        screen.blit(self.sprite, (self.x, self.y)) 
        


