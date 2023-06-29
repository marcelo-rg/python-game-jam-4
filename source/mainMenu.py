import pygame
import sys
from pygame.locals import *
from game import Game
import variables
import time

# Class for the Button
class Button:
	def __init__(self, x, y, w, h, text=''):
		self.rect = pygame.Rect(x, y, w, h)
		self.color = variables.BLUE
		self.text = text
		self.txt_color = variables.WHITE

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.rect)
		if self.text != '':
			font = pygame.font.Font(None, 20)
			text = font.render(self.text, True, self.txt_color)
			screen.blit(text, (self.rect.x + (self.rect.w / 2 - text.get_width() / 2), self.rect.y + (self.rect.h / 2 - text.get_height() / 2)))

	def is_over(self, pos):
		# Pos is the mouse position or a tuple of (x,y) coordinates
		if self.rect.x < pos[0] < self.rect.x + self.rect.w and self.rect.y < pos[1] < self.rect.y + self.rect.h:
			return True

		return False


class MainMenu:
	def __init__(self, fps=variables.fps):
		# Create a screen object
		self.screen_info = pygame.display.Info()
		self.screen_width = self.screen_info.current_w
		self.screen_height = self.screen_info.current_h
		# Set the variables module screen size
		variables.screen_width = self.screen_width
		variables.screen_height = self.screen_height
		print("Screen size: {} x {}".format(variables.screen_width, variables.screen_height)) # Debugging

		self.display = pygame.display.set_mode((self.screen_width, self.screen_height))

		# Define your buttons as instance variables here
		self.play_button = Button(0, 0, 200, 50, 'PLAY')
		#self.options_button = Button(0, 0, 200, 50, 'OPTIONS')
		self.quit_button = Button(0, 0, 200, 50, 'QUIT')

	def start(self):
		self.running = True
		
		#screen_width, screen_height = self.display.get_size()

		# Load the background image
		background_image = pygame.image.load(variables.menu_background_image)
		scaled_background = pygame.transform.scale(background_image, (self.screen_width, self.screen_height))

		# Calculate the positions of the buttons
		button_x = (self.screen_width - self.play_button.rect.width) // 2
		#button_y = (screen_height - (self.play_button.rect.height + self.options_button.rect.height + self.quit_button.rect.height + 20)) // 2
		button_y = (self.screen_height - (self.play_button.rect.height + self.quit_button.rect.height + 20)) // 2

		self.play_button.rect.topleft = (button_x, button_y)
		#self.options_button.rect.topleft = (button_x, button_y + self.play_button.rect.height + 10)
		#self.quit_button.rect.topleft = (button_x, button_y + (self.play_button.rect.height + self.options_button.rect.height + 20))
		self.quit_button.rect.topleft = (button_x, button_y + (self.play_button.rect.height + 20))

		self.display.fill((0, 0, 0))
		self.display.blit(scaled_background, (0, 0))

		# Add the title above the buttons
		self.render_title(variables.game_name, 125, variables.TITLE_COLOR, 100)  # Adjust the size and position as needed

		self.play_button.draw(self.display)
		#self.options_button.draw(self.display)
		self.quit_button.draw(self.display)
		pygame.display.update()

		self.menu_loop()

	def menu_loop(self):
		while True:
			pygame.time.delay(100)

			for event in pygame.event.get():
				pos = pygame.mouse.get_pos()

				if event.type == QUIT:
					pygame.quit()
					sys.exit()

				if event.type == MOUSEBUTTONDOWN:
					if self.play_button.is_over(pos):
						print('Play button clicked')
						self.fade_transition()  # Call the fade transition
						# Create a Game instance and start it
						game = Game(variables.screen_width, variables.screen_height, variables.fps)
						game.start()
						pygame.quit()
						sys.exit()
					#elif self.options_button.is_over(pos):
					#	print('Options button clicked')
					#	# Add options code here
					elif self.quit_button.is_over(pos):
						print('Quit button clicked')
						pygame.quit()
						sys.exit()

				if event.type == MOUSEMOTION:
					if self.play_button.is_over(pos):
						self.play_button.color = variables.GREEN
					else:
						self.play_button.color = variables.BLUE
					#if self.options_button.is_over(pos):
					#	self.options_button.color = variables.GREEN
					#else:
					#	self.options_button.color = variables.BLUE
					if self.quit_button.is_over(pos):
						self.quit_button.color = variables.GREEN
					else:
						self.quit_button.color = variables.BLUE

	def fade_transition(self):
		fade_surface = pygame.Surface((self.screen_width, self.screen_height))
		fade_surface.fill((0, 0, 0))

		for alpha in range(0, 255, 10):
			fade_surface.set_alpha(alpha)
			self.display.blit(fade_surface, (0, 0))
			pygame.display.update()
			time.sleep(0.05)
	
	def render_title(self, text, size, color, y_position):
		font = pygame.font.Font(None, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect(center=(self.screen_width/2, y_position))
		self.display.blit(text_surface, text_rect)