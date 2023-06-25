import pygame
import sys
from pygame.locals import *
from game import Game
import variables

pygame.init()

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
	def __init__(self, screen_width = variables.screen_width, screen_height = variables.screen_height, fps= variables.fps):
		# Initialize Pygame
		pygame.init()
	
	def start(self):
		self.running = True
		self.menu_loop()

	def menu_loop(self):
		while self.running:
			self.handle_events()
			self.update_game_logic()
			self.render()
			self.clock.tick(self.fps)

		pygame.quit()

play_button = Button(50, 50, 200, 50, 'PLAY')
options_button = Button(50, 110, 200, 50, 'OPTIONS')
quit_button = Button(50, 170, 200, 50, 'QUIT')

while True:
	pygame.time.delay(100)

	for event in pygame.event.get():
		pos = pygame.mouse.get_pos()

		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == MOUSEBUTTONDOWN:
			if play_button.is_over(pos):
				print('Play button clicked')
				# Create a Game instance and start it
				game = Game(variables.fps)
				game.start()
			elif options_button.is_over(pos):
				print('Options button clicked')
				# Add options code here
			elif quit_button.is_over(pos):
				print('Quit button clicked')
				pygame.quit()
				sys.exit()

		if event.type == MOUSEMOTION:
			if play_button.is_over(pos):
				play_button.color = variables.GREEN
			else:
				play_button.color = variables.BLUE
			if options_button.is_over(pos):
				options_button.color = variables.GREEN
			else:
				options_button.color = variables.BLUE
			if quit_button.is_over(pos):
				quit_button.color = variables.GREEN
			else:
				quit_button.color = variables.BLUE

	menu.display.fill((0,0,0))
	play_button.draw(menu.display)
	options_button.draw(menu.display)
	quit_button.draw(menu.display)
	pygame.display.update()
