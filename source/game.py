import pygame
import os
import sys
cwd = os.getcwd()

from objects import Planet, Asteroid, Meteor, Spaceship
from sounds import SoundManager
import variables
from player import Player
import random
from pauseMenu import PauseMenu

class Slider:
	def __init__(self, x, y, w, h, text='', value=0, color = variables.LIGHT_GREEN):
		self.rect = pygame.Rect(x, y, w, h)
		self.color = variables.DARK_GREEN  # New color for the bar
		self.txt_color = variables.WHITE
		self.fill_color = color  # New fill color
		#self.fill_color = variables.ANOTHER_GREEN  # New fill color
		self.border_color = variables.BLACK  # New border color
		self.text = text
		self.value = value["current"]/value["max"]  # New value
		self.value_current = value["current"]  # New value
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
		text = font.render(self.text + ": " + str(int(self.value_current)), True, self.txt_color)
		screen.blit(text, (
			self.rect.x + (self.rect.w / 2 - text.get_width() / 2),
			self.rect.y + (self.rect.h / 2 - text.get_height() / 2)
		))


class UI:
	def __init__(self, screen):
		self.screen = screen

		# Initialize sliders with x, y, width, height
		self.slider_p1 = Slider(50, 50, 200, 20, "Player 1 HP", variables.spaceship_one_hp)
		self.slider_p2 = Slider(50, 100, 200, 20, "Player 2 HP", variables.spaceship_two_hp)
		self.slider_planet = Slider(50, 150, 200, 20, "Planet HP", variables.planet_hp)
		self.slider_xp = Slider(50, 200, 200, 20, "XP", variables.initial_xp)
		self.slider_asteroid = Slider(50, 250, 200, 20, "Asteroid HP", variables.asteroid_hp, color = variables.RED)

	def draw(self):
		# Draw each slider on the screen
		self.slider_p1.draw(self.screen)
		self.slider_p2.draw(self.screen)
		self.slider_planet.draw(self.screen)
		self.slider_xp.draw(self.screen)
		self.slider_asteroid.draw(self.screen)

	# def update(self, p1_hp, p2_hp, planet_hp, xp, asteroid_hp):
	# 	# Update slider values
	# 	self.slider_p1.value = p1_hp
	# 	self.slider_p2.value = p2_hp
	# 	self.slider_planet.value = planet_hp
	# 	self.slider_xp.value = xp
	# 	self.slider_asteroid.value = asteroid_hp

	def update(self):
		self.slider_p1.value = variables.spaceship_one_hp["current"]/variables.spaceship_one_hp["max"]  # New value
		self.slider_p1.value_current = variables.spaceship_one_hp["current"]  # New value
		self.slider_p2.value = variables.spaceship_two_hp["current"]/variables.spaceship_two_hp["max"]  # New value
		self.slider_p2.value_current = variables.spaceship_two_hp["current"]  # New value
		self.slider_planet.value = variables.planet_hp["current"]/variables.planet_hp["max"]  # New value
		self.slider_planet.value_current = variables.planet_hp["current"]  # New value
		self.slider_xp.value = variables.initial_xp["current"]/variables.initial_xp["max"]  # New value
		self.slider_xp.value_current = variables.initial_xp["current"]  # New value
		self.slider_asteroid.value = variables.asteroid_hp["current"]/variables.asteroid_hp["max"]  # New value
		self.slider_asteroid.value_current = variables.asteroid_hp["current"]  # New value


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

		# Pause Menu
		self.pause_menu = PauseMenu(self.screen, screen_width, screen_height)

		# Initialize UI
		self.ui = UI(self.screen)
		# Draw UI
		self.ui.draw()

	def handle_events(self):
		for event in pygame.event.get():
			# if event.type == pygame.QUIT:
			# if one presses q key, the game quits
			if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
				self.running = False
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if (event.key == variables.player_controls["Player1"]["Menu"]["Use"] or 
					event.key ==  variables.player_controls["Player2"]["Menu"]["Use"]):
					#print("Game is paused")
					if not self.paused:
						self.sound_player.unpauseBackgroundMusic()
						self.pause_menu.fade_in()
						self.pause()
					elif self.paused:
						self.sound_player.pauseBackgroundMusic()
						self.pause_menu.fade_out()
						self.pause()

	def start(self):
		self.running = True

	def pause(self):
		self.paused = not self.paused

	def restart(self):
		self.running = False
		self.paused = False
		self.start()
	
	def update_game_logic(self):
		if not self.paused:
			# Update game stated
			self.asteroid.update()
			self.planet.update()

			# Update both players
			self.player_one.update("Player1")
			self.player_two.update("Player2")
			
			# Update UI
			self.ui.update()
			# self.ui.update(self.ui.slider_p1.value, self.ui.slider_p2.value, self.ui.slider_planet.value, self.ui.slider_xp.value, self.ui.slider_asteroid.value)
			# update game ui with current values
			# self.ui.update(variables.spaceship_one_hp['current'], variables.spaceship_two_hp['current'], variables.planet_hp['current'], variables.initial_xp['current'], variables.asteroid_hp['current'])

			# Check for collisions between players and spaceships, and handle interaction key presses
			for player, playerID in [(self.player_one, "Player1"), (self.player_two, "Player2")]:
				keys = pygame.key.get_pressed()
				if keys[variables.player_controls[playerID]["Interact"]["Use"]]:
					if player.in_spaceship is not None: # Player is in a spaceship and wants to leave
						if not any(pygame.sprite.collide_circle(player, spaceship) for spaceship in [self.spaceship_one, self.spaceship_two]):
							# Only allow the player to leave the spaceship if they're not currently colliding with another one
							player.leave_spaceship() 
							player.respawn() 
					else: # Player is not in a spaceship and wants to enter
						for spaceship in [self.spaceship_one, self.spaceship_two]:
							if pygame.sprite.collide_circle(player, spaceship):
								player.enter_spaceship(spaceship, playerID)
								break
			
			# Check for upgrade key
			if variables.initial_xp['current']>= variables.initial_xp['max']: # Assuming 'u' is the upgrade key
				self.spaceship_one.upgrade(variables.spaceship_one_asset_upgrade)
				self.spaceship_two.upgrade(variables.spaceship_two_asset_upgrade)
					# for bullet in player.in_spaceship.bullets:
					# 	bullet.upgrade('path_to_new_bullet_sprite')  # Use the correct path to the new bullet sprite

			for meteor in self.meteors:
				meteor.update()
				# Check for collisions with the planet
				if pygame.sprite.collide_circle(meteor, self.planet):
					self.sound_player.playSoundEffect("meteor_impact_" + str(random.randint(1, 5)))
					meteor.respawn()
					variables.planet_hp['current'] -= variables.planet_hp['damage_per_hit']

				# Check for collisions between bullets and meteors/planet/asteroid
				for spaceship in [self.spaceship_one, self.spaceship_two]:
					for bullet in spaceship.bullets:
						if pygame.sprite.collide_circle(meteor, bullet) or \
						pygame.sprite.collide_circle(self.planet, bullet) or \
						pygame.sprite.collide_circle(self.asteroid, bullet):
							bullet.remove()
							if pygame.sprite.collide_circle(meteor, bullet):
								self.sound_player.playSoundEffect("meteor_blast")
								meteor.respawn()
							break

			# Update both spaceships and check for collisions with the asteroid
			for spaceship in [self.spaceship_one, self.spaceship_two]:
				spaceship.update()
				if pygame.sprite.collide_circle(spaceship, self.asteroid):
					spaceship.reposition()
					if spaceship == self.spaceship_one:
						variables.spaceship_one_hp['current'] = 0
					elif spaceship == self.spaceship_two:
						variables.spaceship_two_hp['current'] = 0

	def render(self):
		# Blit the background image to the screen
		self.screen.blit(self.background_image, (0, 0))
		
		# Draw UI
		self.ui.draw()

	def game_loop(self):
		while self.running:
			self.handle_events()
			if not self.paused:
				self.update_game_logic()
				self.render()
			else:
				self.pause_menu.draw_menu()
			self.clock.tick(self.fps)

class TutorialLevel(Level):
	def __init__(self, screen_width=None, screen_height=None, fps=variables.fps, level=None):
		super().__init__(screen_width, screen_height, fps)

		ast_sprite = pygame.image.load(os.path.join(cwd, variables.asteroid_asset))
		self.asteroid = Asteroid(ast_sprite, screen_width // 2, screen_height // 2)

		planet_sprite = pygame.image.load(os.path.join(cwd, variables.planet_asset))
		self.planet = Planet(planet_sprite, screen_width // 2, screen_height // 2)

		# Other Tutorial Level specific initialization...
		self.music_player = SoundManager(variables.sounds)
		self.music_player.loadBackgroundMusic(0,variables.background_music)

	def start(self):
		super().start()
		print("Tutorial Level Initialized")
		self.music_player.playBackgroundMusic()
		self.game_loop()

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
		self.sound_player.loadBackgroundMusic(1,variables.background_music)

	def start(self):
		super().start()
		print("Level 1 Initialized")
		self.sound_player.playBackgroundMusic()
		self.game_loop()

	def handle_events(self):
		super().handle_events()
		# Level 1 specific event handling...

	def update_game_logic(self):
		super().update_game_logic()


	def render(self):
		super().render()

		# Add your rendering code here
		self.asteroid.render(self.screen)
		self.planet.render(self.screen)
		self.spaceship_one.render(self.screen)
		self.spaceship_two.render(self.screen)
		
		# Only render players when they are not inside a spaceship
		if self.player_one.in_spaceship is None:
			self.player_one.render(self.screen)
		if self.player_two.in_spaceship is None:
			self.player_two.render(self.screen)
		
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
		self.sound_player.loadBackgroundMusic(2,variables.background_music)

	def start(self):
		super().start()
		print("Level 2 Initialized")
		self.sound_player.playBackgroundMusic()
		self.game_loop()

	def handle_events(self):
		super().handle_events()
		# Level 2 specific event handling...

	def update_game_logic(self):
		super().update_game_logic()


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
		self.current_level = level
		if self.current_level == "None":
			#print("Tutorial level started")
			self.current_level = TutorialLevel(screen_width, screen_height, fps, level)  # Starts with Tutorial Level
		elif self.current_level == "One":
			self.current_level = LevelOne(screen_width, screen_height, fps, level)  # Starts with Level One
		elif self.current_level == "Two":
			self.current_level = LevelTwo(screen_width, screen_height, fps, level)  # Starts with Level Two
		else:
			print("Invalid level name")
			pygame.quit()
			sys.exit()

	def start(self):
		self.current_level.start()

#if __name__ == "__main__":
	# Create a game instance and start it
#	game = Game(fps = variables.fps)
#	game.start()
