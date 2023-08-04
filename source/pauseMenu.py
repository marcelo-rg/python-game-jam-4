import pygame
import sys
from pygame.locals import *
import variables
from sounds import SoundManager

# Class for the Button
class ButtonPM:
	def __init__(self, x, y, w, h, text='', sound_manager=None, hover_sound=None):
		self.rect = pygame.Rect(x, y, w, h)
		self.color = variables.DARK_GREEN
		self.hover_color = variables.DARKER_GREEN
		self.clicked_color = variables.TITLE_COLOR  # Add a new color for when the button is clicked
		self.current_color = self.color
		self.text = text
		self.txt_color = variables.WHITE
		self.clicked = False  # New click state flag
		self.hover_sound = hover_sound

		# Sound effects
		self.sound_manager = sound_manager
		self.hovered = False
		self.hovered_button = None

	def draw(self, screen):
		pygame.draw.rect(screen, self.current_color, self.rect)
		if self.text != '':
			font_size = min(int(self.rect.height * 0.9), int(self.rect.width * 0.80))
			font = pygame.font.Font(None, font_size)
			text = font.render(self.text, True, self.txt_color)
			screen.blit(text, (
				self.rect.x + (self.rect.w / 2 - text.get_width() / 2),
				self.rect.y + (self.rect.h / 2 - text.get_height() / 2)
			))

	def is_over(self, pos):
		return self.rect.collidepoint(pos)

	def handle_event(self, event, pos):
		if self.is_over(pos):
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.clicked = True
				self.current_color = self.clicked_color
				self.sound_manager.playSoundEffect("click_button")
			elif event.type == pygame.MOUSEBUTTONUP:
				if self.clicked:
					self.clicked = False
					if self.is_hover(pos):
						self.current_color = self.hover_color
					else:
						self.current_color = self.color
					return True
		else:
			self.clicked = False
			self.hovered = False  # Reset hovered state
			self.current_color = self.color  # Set default color

		if self.is_hover(pos):
			if not self.clicked:
				self.current_color = self.hover_color
			if not self.hovered:
				self.hovered = True
				if self.hover_sound:
					self.sound_manager.playSoundEffect(self.hover_sound)
				if self.hovered_button and self.hovered_button != self:
					self.hovered_button.hovered = False
					self.hovered_button.current_color = self.hovered_button.color
				self.hovered_button = self
		else:
			if not self.clicked:
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
	
	def reset(self):
		self.clicked = False
		self.current_color = self.color
		self.hovered = False


class PauseMenu:
	def __init__(self, screen, screen_width, screen_height):
		# Initialize the PauseMenu
		self.screen = screen
		self.width = screen_width
		self.height = screen_height

		# Initialize buttons
		button_width = self.width // 3
		button_height = self.height // 10

		# Music
		self.sound_player = SoundManager(variables.sounds)

		# Define the buttons as instance variables
		self.resume_button = ButtonPM(self.width // 2 - button_width // 2, self.height * 1 // 5, button_width, button_height, "Resume", self.sound_player, "play_button")
		self.restart_button = ButtonPM(self.width // 2 - button_width // 2, self.height * 2 // 5, button_width, button_height, "Restart", self.sound_player, "option_button")
		self.main_menu_button = ButtonPM(self.width // 2 - button_width // 2, self.height * 3 // 5, button_width, button_height, "Main Menu", self.sound_player, "quit_button")
		self.quit_button = ButtonPM(self.width // 2 - button_width // 2, self.height * 4 // 5, button_width, button_height, "Quit", self.sound_player, "quit_button")

	def draw_menu(self):
		# Draw the pause menu on the screen
		self.resume_button.draw(self.screen)
		self.restart_button.draw(self.screen)
		self.main_menu_button.draw(self.screen)
		self.quit_button.draw(self.screen)

	def handle_event(self, event):
		pos = pygame.mouse.get_pos()

		if self.resume_button.handle_event(event, pos):
			# Resume game
			self.fade_out()  # Hide the pause menu
			return 1
			# Continue the game loop here
		elif self.restart_button.handle_event(event, pos):
			# Restart game
			self.fade_out()  # Hide the pause menu
			return 2
			# Reset the game state and start the game loop here
		elif self.main_menu_button.handle_event(event, pos):
			# Go to main menu
			self.fade_out()  # Hide the pause menu
			return 3
			# Load the main menu here
		elif self.quit_button.handle_event(event, pos):
			# Quit game
			pygame.quit()
			sys.exit()
		return 0  # No action was performed

	def fade_in(self):
		fade = pygame.Surface((self.width, self.height))
		fade.fill((0, 0, 0))
		for alpha in range(0, 128, 10):
			fade.set_alpha(alpha)
			self.draw_menu()
			self.screen.blit(fade, (0, 0))
			pygame.display.update()

	def fade_out(self):
		fade = pygame.Surface((self.width, self.height))
		fade.fill((0, 0, 0))
		for alpha in range(120, -1, -10):
			fade.set_alpha(alpha)
			self.draw_menu()
			self.screen.blit(fade, (0, 0))
			pygame.display.update()

