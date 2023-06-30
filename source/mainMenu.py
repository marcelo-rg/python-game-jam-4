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
		self.color = variables.DARK_GREEN
		self.hover_color = variables.DARKER_GREEN
		self.clicked_color = variables.TITLE_COLOR  # Add a new color for when the button is clicked
		self.current_color = self.color
		self.text = text
		self.txt_color = variables.WHITE
		        self.clicked = False  # New click state flag

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
	
	def handle_event(self, event, pos):
		if self.is_over(pos):
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.current_color = self.clicked_color
			elif event.type == pygame.MOUSEBUTTONUP:
				return True
			else:
				self.current_color = self.hover_color
		else:
			self.current_color = self.color
		return False
	
	def is_hover(self, pos):
		if self.rect.x < pos[0] < self.rect.x + self.rect.w and self.rect.y < pos[1] < self.rect.y + self.rect.h:
			return True
		return False

	def is_click(self, pos, event):
		if self.is_hover(pos) and event.type == pygame.MOUSEBUTTONDOWN:
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
		self.options_button = Button(0, 0, 200, 50, 'OPTIONS')
		self.quit_button = Button(0, 0, 200, 50, 'QUIT')

	def start(self):
		self.running = True

		# Load the background image
		background_image = pygame.image.load(variables.menu_background_image)
		self.scaled_background = pygame.transform.scale(background_image, (self.screen_width, self.screen_height))

		# Calculate the positions of the buttons
		button_x = (self.screen_width - self.play_button.rect.width) // 2
		button_y = (self.screen_height - (self.play_button.rect.height + self.options_button.rect.height + self.quit_button.rect.height + 20)) // 2

		self.play_button.rect.topleft = (button_x, button_y)
		self.options_button.rect.topleft = (button_x, button_y + self.play_button.rect.height + 10)
		self.quit_button.rect.topleft = (button_x, button_y + (self.play_button.rect.height + self.options_button.rect.height + 20))

		self.display.fill((0, 0, 0))
		self.display.blit(self.scaled_background, (0, 0))

		self.play_button.draw(self.display)
		self.options_button.draw(self.display)
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

				if self.play_button.handle_event(event, pos):
					print('Play button clicked')
					self.fade_transition()
					game = Game(variables.screen_width, variables.screen_height, variables.fps)
					game.start()
					pygame.quit()
					sys.exit()

				if self.options_button.handle_event(event, pos):  # Add this line
					print('Options button clicked')
					# Add options code here

				if self.quit_button.handle_event(event, pos):
					print('Quit button clicked')
					pygame.quit()
					sys.exit()

				# Handle button hover and click colors
				if event.type == MOUSEMOTION:
					if self.play_button.is_hover(pos):
						self.play_button.color = variables.DARKER_GREEN
					else:
						self.play_button.color = variables.DARK_GREEN
					if self.options_button.is_hover(pos):
						self.options_button.color = variables.DARKER_GREEN
					else:
						self.options_button.color = variables.DARK_GREEN
					if self.quit_button.is_hover(pos):
						self.quit_button.color = variables.DARKER_GREEN
					else:
						self.quit_button.color = variables.DARK_GREEN

				if event.type == MOUSEBUTTONDOWN:
					if self.play_button.is_click(pos, event):
						self.play_button.color = variables.TITLE_COLOR
					if self.options_button.is_click(pos, event):
						self.options_button.color = variables.TITLE_COLOR
					if self.quit_button.is_click(pos, event):
						self.quit_button.color = variables.TITLE_COLOR
					pygame.display.update()  # Move the display update here

				if event.type == MOUSEBUTTONUP:
					if self.play_button.is_click(pos, event):
						print('Play button clicked')
						self.fade_transition()
						game = Game(variables.screen_width, variables.screen_height, variables.fps)
						game.start()
						pygame.quit()
						sys.exit()
					if self.options_button.is_over(pos):
						print('Options button clicked')
						# Add options code here
					if self.quit_button.is_click(pos, event):
						print('Quit button clicked')
						pygame.quit()
						sys.exit()

			# Update the screen
			self.display.fill((0, 0, 0))
			self.display.blit(self.scaled_background, (0, 0))
			self.render_title(variables.game_name, 125, variables.TITLE_COLOR, 100)
			self.play_button.draw(self.display)
			self.options_button.draw(self.display)  # Add this line
			self.quit_button.draw(self.display)
			pygame.display.update()


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