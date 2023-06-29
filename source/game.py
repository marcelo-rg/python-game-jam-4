import pygame
import os 
cwd = os.getcwd()

from objects import Planet, Asteroid, Meteor, Spaceship
from sounds import *
from background import Background
import variables
from player import Player

class Game:
	def __init__(self, screen_width = None, screen_height = None, fps= variables.fps):
		# Initialize Pygame
		pygame.init()

		if screen_width is None or screen_height is None:
			# Get the screen size
			screen_info = pygame.display.Info()
			screen_width = screen_info.current_w
			screen_height = screen_info.current_h
			
			# Set the variables module screen size
			variables.screen_width = screen_width
			variables.screen_height = screen_height
			print("Screen size: {} x {}".format(variables.screen_width, variables.screen_height)) # Debugging

		# Music
		self.sound_player = SoundManager(variables.sounds)
		self.sound_player.loadBackgroundMusic(os.path.join(variables.sound_path, variables.background_music))
		self.sound_player.playBackgroundMusic()

		# Set up the game window
		self.screen = pygame.display.set_mode((screen_width, screen_height))
		pygame.display.set_caption(variables.game_name)

		# Set up the game clock
		self.clock = pygame.time.Clock()
		self.fps = fps

		# Game state
		self.running = False 
		self.paused = False

		# Load the background image
		self.background_image = pygame.image.load(variables.background_image).convert()
		self.background_image = pygame.transform.scale(self.background_image, (screen_width, screen_height))
	
		# Add game elements here
		ast_sprite = pygame.image.load(os.path.join(cwd, variables.asteroid_asset))
		self.asteroid = Asteroid(ast_sprite, screen_width // 2, screen_height // 2)

		planet_sprite = pygame.image.load(os.path.join(cwd, variables.planet_asset))
		self.planet = Planet(planet_sprite, screen_width // 2, screen_height // 2)

		meteors_sprite_list = [pygame.image.load( \
				os.path.join(variables.meteor_big_asset + str(iterable) + variables.png_extension)) \
				for iterable in range(1,4,1)]
		self.meteors = [Meteor(meteors_sprite_list[iterable], screen_width, screen_height, self.planet.rect.centerx, self.planet.rect.centery) \
		  		for iterable in range(len(meteors_sprite_list))]		

		# Players
		self.player_one = Player("Player1", variables.player_speed, variables.player_assets["Player1"],
			   						self.planet.radius,
			   						(self.planet.rect.centerx,
									self.planet.rect.centery)
								)
		self.player_two = Player("Player2", variables.player_speed, variables.player_assets["Player2"],
			   						self.planet.radius,
			   						(self.planet.rect.centerx,
									self.planet.rect.centery)
								)
    
		# Spaceships
		self.spaceship_one = Spaceship(1,0,variables.spaceship_speed, variables.spaceship_one_asset, screen_width=screen_width, screen_height=screen_height, sound_manager= self.sound_player)
		self.spaceship_two = Spaceship(1,1,variables.spaceship_speed, variables.spaceship_two_asset, screen_width=screen_width, screen_height=screen_height, sound_manager= self.sound_player)

	def start(self):
		self.running = True
		self.game_loop()

	def pause(self):
		self.paused = not self.paused

	def restart(self):
		self.running = False
		self.paused = False
		self.start()

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYDOWN:
				#if event.key == pygame.K_p:
				#	self.pause()
				#elif event.key == pygame.K_r:
				#	self.restart()
				#elif event.key == pygame.K_w:
				#	print("Move the character forwards")
				#elif event.key == pygame.K_s:
				#	print("Move the character backwards")
				#elif event.key == pygame.K_a:
				#	print("Move the character left")
				#elif event.key == pygame.K_d:
				#	print("Move the character right")
				if event.key == pygame.K_q:
					self.running = False


	def update_game_logic(self):
		if not self.paused:
			# Update game stated
			# keys_pressed = pygame.key.get_pressed()
			self.asteroid.update()
			self.planet.update()
			for meteor in self.meteors:
				# Check for collisions
				if pygame.sprite.collide_circle(meteor, self.planet):
					self.sound_player.playSoundEffect("meteor_impact")
					meteor.respawn()
				meteor.update()
		# check for collisions between spaceships and planet
		collide_one = pygame.sprite.collide_circle(self.spaceship_one, self.planet)
		collide_two = pygame.sprite.collide_circle(self.spaceship_two, self.planet)

		self.spaceship_one.update()
		self.spaceship_two.update()

		self.player_one.update("Player1")
		self.player_two.update("Player2") 


	def render(self):
		# Render the game elements
    # Set the screen to black
		#self.screen.fill((0, 0, 0))  # Example background fill

		 # Blit the background image to the screen
		self.screen.blit(self.background_image, (0, 0))

		# Add your rendering code here
		self.asteroid.render(self.screen)
		self.planet.render(self.screen)
		self.player_one.render(self.screen)
		self.player_two.render(self.screen)
		self.spaceship_one.render(self.screen)
		self.spaceship_two.render(self.screen)
		for meteor in self.meteors:
			meteor.render(self.screen)

		# Update the screen
		pygame.display.flip()

	def game_loop(self):
		while self.running:
			self.handle_events()
			self.update_game_logic()
			self.render()
			self.clock.tick(self.fps)

		pygame.quit()

if __name__ == "__main__":
	# Create a game instance and start it
	game = Game(fps = variables.fps)
	game.start()
