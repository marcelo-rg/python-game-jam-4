import pygame
import sys
from pygame.locals import *
from game import Game
import variables
import time
from sounds import SoundManager

# Class for the Button
class Button:
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

		# Music
		self.sound_player = SoundManager(variables.sounds)
		self.sound_player.loadMenuBackgroundMusic(variables.pause_menu_music)
		self.sound_player.playBackgroundMusic()

		# Define your buttons as instance variables here
		self.play_button = Button(0, 0, 200, 50, 'PLAY', self.sound_player, "play_button")
		self.options_button = Button(0, 0, 200, 50, 'OPTIONS', self.sound_player, "option_button")
		self.quit_button = Button(0, 0, 200, 50, 'QUIT', self.sound_player, "quit_button")

		# Initialize menu state
		self.menu_state = "main"
		self.options_menu = OptionsMenu(self.display, self.sound_player, self.back_to_main_menu)

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

		# Reset button states
		self.play_button.reset()
		self.options_button.reset()
		self.quit_button.reset()

		self.play_button.draw(self.display)
		self.options_button.draw(self.display)
		self.quit_button.draw(self.display)
		pygame.display.update()

		self.menu_loop()

		pygame.quit()
		sys.exit()

	def menu_loop(self):
		while True:
			#pygame.time.delay(100)
			pos = pygame.mouse.get_pos()
			
			for event in pygame.event.get():
				if event.type == QUIT:
					self.running = False
					return

				if self.menu_state == "main":
					if self.play_button.handle_event(event, pos):
						print('Play button clicked')
						self.fade_transition()
						game = Game(variables.screen_width, variables.screen_height, variables.fps)
						game.start()
						self.running = False
						return

					if self.options_button.handle_event(event, pos):
						print('Options button clicked')
						self.menu_state = "options"
						self.options_menu.reset_buttons()  # Reset the buttons in the options menu
					
					if self.quit_button.handle_event(event, pos):
						print('Quit button clicked')
						self.running = False
						return

				elif self.menu_state == "options":
					if self.options_menu.handle_event(event, pos):  # If back button is clicked in options menu
						self.menu_state = "main"
						self.play_button.reset()   # Reset the buttons in the main menu
						self.options_button.reset()
						self.quit_button.reset()

			# Update the screen outside the event loop
			self.display.fill((0, 0, 0))
			self.display.blit(self.scaled_background, (0, 0))
			
			if self.menu_state == "main":
				self.render_title(variables.game_name, 125, variables.TITLE_COLOR, 100)
				self.play_button.draw(self.display)
				self.options_button.draw(self.display)
				self.quit_button.draw(self.display)
			elif self.menu_state == "options":
				self.render_title(variables.options_menu_name, 125, variables.TITLE_COLOR, 100)
				self.options_menu.draw()

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
	
	def back_to_main_menu(self):
		self.menu_state = "main"


class Slider:
	def __init__(self, x, y, w, h, text='', sound_manager=None, value=0, slider_type=''):
		self.rect = pygame.Rect(x, y, w, h)
		self.color = variables.DARK_GREEN
		self.txt_color = variables.WHITE
		#self.fill_color = variables.LIGHT_GREEN  # New fill color
		self.fill_color = variables.ANOTHER_GREEN  # New fill color
		self.border_color = variables.BLACK  # New border color
		self.text = text
		self.value = value
		self.sound_manager = sound_manager
		self.slider_type = slider_type  # Added slider type
		self.border_width = 2  # New border width

	def draw(self, screen):
		# Draw the border
		pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
		
		# Draw the fill bar
		fill_rect = pygame.Rect(self.rect.x + self.border_width, self.rect.y + self.border_width,
								(self.rect.w - 2 * self.border_width) * self.value,
								self.rect.h - 2 * self.border_width)
		pygame.draw.rect(screen, self.fill_color, fill_rect)

		# Draw the text
		font_size = min(int(self.rect.height * 0.9), int(self.rect.width * 0.80))
		font = pygame.font.Font(None, font_size)
		text = font.render(self.text + ": " + str(int(self.value * 100)), True, self.txt_color)
		screen.blit(text, (
			self.rect.x + (self.rect.w / 2 - text.get_width() / 2),
			self.rect.y + (self.rect.h / 2 - text.get_height() / 2)
		))

	def handle_event(self, event, pos):
		if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos):
			old_value = self.value
			self.value = max(0, min((pos[0] - (self.rect.x + self.border_width)) / (self.rect.w - 2 * self.border_width), 1))
			if self.slider_type == 'music' and old_value != self.value:  # Check if slider type is music and the value has changed
				print("Music volume was changed to: " + str(self.value))
				variables.music_slider = self.value
				self.sound_manager.setMusicVolume(variables.music_slider, variables.global_music_volume)
			elif self.slider_type == 'sfx' and old_value != self.value:  # Check if slider type is sfx and the value has changed
				print("SFX volume was changed to: " + str(self.value))
				variables.sound_effect_slider = self.value
			return True
		return False

class OptionsMenu:
	def __init__(self, display, sound_player, back_callback):
		self.display = display
		self.sound_player = sound_player
		self.back_button = Button(0, 0, 200, 50, 'BACK', sound_player, "option_button")
		self.music_slider = Slider(0, 0, 400, 50, 'Music Volume', sound_player, variables.music_slider, 'music')
		self.sfx_slider = Slider(0, 0, 400, 50, 'SFX Volume', sound_player, variables.sound_effect_slider, 'sfx')
		self.back_callback = back_callback
		
		# Set the positions of the buttons and sliders before drawing them.
		screen_width, screen_height = self.display.get_size()
		self.slider_x = (screen_width - self.music_slider.rect.width) // 2
		self.button_y = (screen_height - (self.back_button.rect.height + self.music_slider.rect.height + self.sfx_slider.rect.height + 20)) // 2
		self.music_slider.rect.topleft = (self.slider_x, self.button_y)
		self.sfx_slider.rect.topleft = (self.slider_x, self.button_y + self.music_slider.rect.height + 10)
		
		self.button_x = self.music_slider.rect.x + (self.music_slider.rect.width - self.back_button.rect.width) // 2
		self.back_button.rect.topleft = (self.button_x, self.button_y + (self.music_slider.rect.height + self.sfx_slider.rect.height + 20))	

	def draw(self):
		# Now you can draw them.
		self.music_slider.draw(self.display)
		self.sfx_slider.draw(self.display)
		self.back_button.draw(self.display)

	def handle_event(self, event, pos):
		if self.back_button.handle_event(event, pos):
			self.back_callback()
			self.reset_buttons()  # Reset the buttons in the options menu
			return True
		self.music_slider.handle_event(event, pos)
		self.sfx_slider.handle_event(event, pos)
		return False

	def reset_buttons(self):
		self.back_button.reset()