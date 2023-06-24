import pygame

class Asteroid:
    def __init__(self, x, y, image_path):
        self.position = pygame.Vector2(x, y)
        self.sprite = pygame.image.load(image_path)

    def update(self, keys_pressed):
        # Update the position based on user input or game logic
        if keys_pressed[pygame.K_w]:
            self.position.y -= 1
        elif keys_pressed[pygame.K_s]:
            self.position.y += 1
        elif keys_pressed[pygame.K_a]:
            self.position.x -= 1
        elif keys_pressed[pygame.K_d]:
            self.position.x += 1

    def draw(self, screen):
        # Draw the object on the screen
        screen.blit(self.sprite, self.position)
