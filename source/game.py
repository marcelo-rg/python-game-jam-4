import pygame
import os
import sys
cwd = os.getcwd()

from objects import Planet, Asteroid, Meteor, Spaceship
from sounds import SoundManager
import variables
from player import Player
import random

class Level:
	def __init__(self, screen_width=None, screen_height=None, fps=variables.fps):
		# Initialize Pygame
		pygame.init()

		# Common screen dimensions setup
		if screen_width is None or screen_height is None:
			# Get the screen size
			screen_info = pygame.display.Info()
			screen_width = screen_info.current_w
			screen_height = screen_info.current_h

			# Set the variables module screen size
			variables.screen_width = screen_width
			variables.screen_height = screen_height

		# Music
		self.sound_player = SoundManager(variables.sounds)
		self.sound_player.loadBackgroundMusic(1,variables.background_music)
		self.sound_player.playBackgroundMusic()

		# Set up the game window
		self.screen = pygame.display.set_mode((screen_width, screen_height))
		pygame.display.set_caption(variables.game_name)

		# Set up the game clock
		self.clock = pygame.time.Clock()
		self.fps = fps

		self.running = False 
		self.paused = False

		# Background
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
		self.spaceship_one = Spaceship(1,0,variables.spaceship_speed, variables.spaceship_one_asset, screen_width=screen_width, screen_height=screen_height, sound_manager= self.sound_player, planet_radius=self.planet.radius)
		self.spaceship_two = Spaceship(1,1,variables.spaceship_speed, variables.spaceship_two_asset, screen_width=screen_width, screen_height=screen_height, sound_manager= self.sound_player, planet_radius=self.planet.radius)

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					self.running = False
					pygame.quit()
					sys.exit()

	def start(self):
		self.running = True
		self.game_loop()

	def pause(self):
		self.paused = not self.paused

	def restart(self):
		self.running = False
		self.paused = False
		self.start()
	
	def update_game_logic(self):
		pass

	def render(self):
		# Blit the background image to the screen
		self.screen.blit(self.background_image, (0, 0))

	def game_loop(self):
		while self.running:
			self.handle_events()
			self.update_game_logic()
			self.render()
			self.clock.tick(self.fps)


class TutorialLevel(Level):
	def __init__(self, screen_width=None, screen_height=None, fps=variables.fps, level=None):
		super().__init__(screen_width, screen_height, fps)

		ast_sprite = pygame.image.load(os.path.join(cwd, variables.asteroid_asset))
		self.asteroid = Asteroid(ast_sprite, screen_width // 2, screen_height // 2)

		planet_sprite = pygame.image.load(os.path.join(cwd, variables.planet_asset))
		self.planet = Planet(planet_sprite, screen_width // 2, screen_height // 2)

		# Other Tutorial Level specific initialization...

	def handle_events(self):
		super().handle_events()
		# Tutorial Level specific event handling...

	def update_game_logic(self):
		super().update_game_logic()

		if not self.paused:
			# Update game stated
			self.asteroid.update()
			self.planet.update()

			for meteor in self.meteors:
				# Check for collisions
				if pygame.sprite.collide_circle(meteor, self.planet):
					random_number = random.randint(1, 5)
					self.sound_player.playSoundEffect("meteor_impact_"+random_number.__str__())
					meteor.respawn()

				# Check for collisions between bullets and meteors
				for bullet in self.spaceship_one.bullets + self.spaceship_two.bullets:
					if pygame.sprite.collide_circle(meteor, bullet):
						meteor.respawn()
						self.sound_player.playSoundEffect("meteor_blast")
						bullet.remove() # You will need to implement a remove() method in the Bullet class
					if pygame.sprite.collide_circle(self.planet, bullet) or pygame.sprite.collide_circle(self.asteroid, bullet):
						bullet.remove()

				meteor.update()

			# check for collisions between spaceships and asteroid
			if pygame.sprite.collide_circle(self.spaceship_one, self.asteroid):
				self.spaceship_one.reposition()  
			if pygame.sprite.collide_circle(self.spaceship_two, self.asteroid):
				self.spaceship_two.reposition() 

			self.spaceship_one.update()
			self.spaceship_two.update()

			self.player_one.update("Player1")
			self.player_two.update("Player2")

	def render(self):
		super().render()

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

class LevelOne(Level):
	def __init__(self, screen_width=None, screen_height=None, fps=variables.fps, level=None):
		super().__init__(screen_width, screen_height, fps)

		ast_sprite = pygame.image.load(os.path.join(cwd, variables.asteroid_asset))
		self.asteroid = Asteroid(ast_sprite, screen_width // 2, screen_height // 2)

		planet_sprite = pygame.image.load(os.path.join(cwd, variables.planet_asset))
		self.planet = Planet(planet_sprite, screen_width // 2, screen_height // 2)

		# Other Level 1 specific initialization...

	def handle_events(self):
		super().handle_events()
		# Level 1 specific event handling...

	def update_game_logic(self):
		super().update_game_logic()

		if not self.paused:
			# Update game stated
			self.asteroid.update()
			self.planet.update()

			for meteor in self.meteors:
				# Check for collisions
				if pygame.sprite.collide_circle(meteor, self.planet):
					random_number = random.randint(1, 5)
					self.sound_player.playSoundEffect("meteor_impact_"+random_number.__str__())
					meteor.respawn()

				# Check for collisions between bullets and meteors
				for bullet in self.spaceship_one.bullets + self.spaceship_two.bullets:
					if pygame.sprite.collide_circle(meteor, bullet):
						meteor.respawn()
						self.sound_player.playSoundEffect("meteor_blast")
						bullet.remove() # You will need to implement a remove() method in the Bullet class
					if pygame.sprite.collide_circle(self.planet, bullet) or pygame.sprite.collide_circle(self.asteroid, bullet):
						bullet.remove()

				meteor.update()

			# check for collisions between spaceships and asteroid
			if pygame.sprite.collide_circle(self.spaceship_one, self.asteroid):
				self.spaceship_one.reposition()  
			if pygame.sprite.collide_circle(self.spaceship_two, self.asteroid):
				self.spaceship_two.reposition() 

			self.spaceship_one.update()
			self.spaceship_two.update()

			self.player_one.update("Player1")
			self.player_two.update("Player2")

	def render(self):
		super().render()

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

class LevelTwo(Level):
	def __init__(self, screen_width=None, screen_height=None, fps=variables.fps, level=None):
		super().__init__(screen_width, screen_height, fps)

		ast_sprite = pygame.image.load(os.path.join(cwd, variables.asteroid_asset))
		self.asteroid = Asteroid(ast_sprite, screen_width // 2, screen_height // 2)

		planet_sprite = pygame.image.load(os.path.join(cwd, variables.planet_asset))
		self.planet = Planet(planet_sprite, screen_width // 2, screen_height // 2)

		# Other Level 2 specific initialization...

	def handle_events(self):
		super().handle_events()
		# Level 2 specific event handling...

	def update_game_logic(self):
		super().update_game_logic()

		if not self.paused:
			# Update game stated
			self.asteroid.update()
			self.planet.update()

			for meteor in self.meteors:
				# Check for collisions
				if pygame.sprite.collide_circle(meteor, self.planet):
					random_number = random.randint(1, 5)
					self.sound_player.playSoundEffect("meteor_impact_"+random_number.__str__())
					meteor.respawn()

				# Check for collisions between bullets and meteors
				for bullet in self.spaceship_one.bullets + self.spaceship_two.bullets:
					if pygame.sprite.collide_circle(meteor, bullet):
						meteor.respawn()
						self.sound_player.playSoundEffect("meteor_blast")
						bullet.remove() # You will need to implement a remove() method in the Bullet class
					if pygame.sprite.collide_circle(self.planet, bullet) or pygame.sprite.collide_circle(self.asteroid, bullet):
						bullet.remove()

				meteor.update()

			# check for collisions between spaceships and asteroid
			if pygame.sprite.collide_circle(self.spaceship_one, self.asteroid):
				self.spaceship_one.reposition()  
			if pygame.sprite.collide_circle(self.spaceship_two, self.asteroid):
				self.spaceship_two.reposition() 

			self.spaceship_one.update()
			self.spaceship_two.update()

			self.player_one.update("Player1")
			self.player_two.update("Player2")

	def render(self):
		super().render()

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

class Game:
	def __init__(self, screen_width=None, screen_height=None, fps=variables.fps, level="None"):
		self.levels = [TutorialLevel(screen_width, screen_height, fps, level), 
		 				LevelOne(screen_width, screen_height, fps, level), 
						LevelTwo(screen_width, screen_height, fps, level)
						]
		self.current_level = level

	def start(self):
		if self.current_level == "None":
			#print("Tutorial level started")
			self.current_level = self.levels[0]  # Starts with Tutorial Level
		elif self.current_level == "One":
			self.current_level = self.levels[1]  # Starts with Level One
		elif self.current_level == "Two":
			self.current_level = self.levels[2]  # Starts with Level Two
		else:
			print("Invalid level name")
			pygame.quit()
			sys.exit()

		self.current_level.running = True
		self.current_level.game_loop()

	def next_level(self):
		current_level_index = self.levels.index(self.current_level)

		if current_level_index < len(self.levels) - 1:
			self.current_level = self.levels[current_level_index + 1]
			self.current_level.game_loop()
		else:
			print("Game completed!")
			pygame.quit()
			sys.exit()

	def restart_level(self):
		self.current_level.restart()

#if __name__ == "__main__":
	# Create a game instance and start it
#	game = Game(fps = variables.fps)
#	game.start()
