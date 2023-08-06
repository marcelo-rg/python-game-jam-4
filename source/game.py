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
import time
from saveGame import SaveGame  # Import the SaveGame class

class Slider:
	def __init__(self, x, y, w, h, text='', value=0, color=variables.LIGHT_GREEN, apply_gradient=False):
		self.rect = pygame.Rect(x, y, w, h)
		self.color = variables.DARK_GREEN  # New color for the bar
		self.txt_color = variables.WHITE
		self.border_color = variables.BLACK  # New border color
		self.text = text
		self.value = value["current"]/value["max"]  # New value
		self.value_current = value["current"]  # New value
		self.border_width = 2  # New border width
		self.fill_color = color
		self.apply_gradient = apply_gradient

	def draw(self, screen):
		# Draw the border
		pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)

		# Draw the fill bar
		fill_rect = pygame.Rect(self.rect.x + self.border_width, self.rect.y + self.border_width,
								(self.rect.w - 2 * self.border_width) * self.value,
								self.rect.h - 2 * self.border_width)

		if self.apply_gradient:
			if self.value <= 0.33:
				self.fill_color = variables.RED
			elif self.value <= 0.67:
				self.fill_color = variables.YELLOW
			else:
				self.fill_color = variables.LIGHT_GREEN

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
		self.slider_p1 = Slider(50, 50, 200, 20, "Spaceship 1 HP", variables.game_data[variables.current_level]["spaceship_one_hp"], apply_gradient=True)
		self.slider_p2 = Slider(50, 100, 200, 20, "Spaceship 2 HP", variables.game_data[variables.current_level]["spaceship_two_hp"], apply_gradient=True)
		self.slider_planet = Slider(50, 150, 200, 20, "Planet HP", variables.game_data[variables.current_level]["planet_hp"], apply_gradient=True)
		self.slider_xp = Slider(50, 200, 200, 20, "XP", variables.game_data[variables.current_level]["initial_xp"], color = variables.YELLOW)
		self.slider_asteroid = Slider(50, 250, 200, 20, "Asteroid HP", variables.game_data[variables.current_level]["asteroid_hp"], color = variables.RED)

	def draw(self):
		# Draw each slider on the screen
		self.slider_p1.draw(self.screen)
		self.slider_p2.draw(self.screen)
		self.slider_planet.draw(self.screen)
		self.slider_xp.draw(self.screen)
		self.slider_asteroid.draw(self.screen)

	def update(self):
		self.slider_p1.value = min(variables.game_data[variables.current_level]["spaceship_one_hp"]["current"], variables.game_data[variables.current_level]["spaceship_one_hp"]["max"])/variables.game_data[variables.current_level]["spaceship_one_hp"]["max"]
		self.slider_p1.value_current = min(variables.game_data[variables.current_level]["spaceship_one_hp"]["current"], variables.game_data[variables.current_level]["spaceship_one_hp"]["max"])

		self.slider_p2.value = min(variables.game_data[variables.current_level]["spaceship_two_hp"]["current"], variables.game_data[variables.current_level]["spaceship_two_hp"]["max"])/variables.game_data[variables.current_level]["spaceship_two_hp"]["max"]
		self.slider_p2.value_current = min(variables.game_data[variables.current_level]["spaceship_two_hp"]["current"], variables.game_data[variables.current_level]["spaceship_two_hp"]["max"])

		self.slider_planet.value = min(variables.game_data[variables.current_level]["planet_hp"]["current"], variables.game_data[variables.current_level]["planet_hp"]["max"])/variables.game_data[variables.current_level]["planet_hp"]["max"]
		self.slider_planet.value_current = min(variables.game_data[variables.current_level]["planet_hp"]["current"], variables.game_data[variables.current_level]["planet_hp"]["max"])

		self.slider_xp.value = min(variables.game_data[variables.current_level]["initial_xp"]["current"], variables.game_data[variables.current_level]["initial_xp"]["max"])/variables.game_data[variables.current_level]["initial_xp"]["max"]
		self.slider_xp.value_current = min(variables.game_data[variables.current_level]["initial_xp"]["current"], variables.game_data[variables.current_level]["initial_xp"]["max"])

		self.slider_asteroid.value = min(variables.game_data[variables.current_level]["asteroid_hp"]["current"], variables.game_data[variables.current_level]["asteroid_hp"]["max"])/variables.game_data[variables.current_level]["asteroid_hp"]["max"]
		self.slider_asteroid.value_current = min(variables.game_data[variables.current_level]["asteroid_hp"]["current"], variables.game_data[variables.current_level]["asteroid_hp"]["max"])

class Level():
	def __init__(self, screen_width=None, screen_height=None, fps=variables.fps, button_level=None):
		# Initialize Pygame
		pygame.init()
		self.button_level = button_level

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

		meteors_sprite_list = [pygame.image.load(
			os.path.join(variables.meteor_big_asset + str(random.randint(1, 3)) + variables.png_extension)
		) for _ in range(variables.game_data[variables.current_level]["num_meteors"])]  # Assuming 'meteor_big_asset' is the path to the meteor sprite
		self.meteors = [Meteor(meteors_sprite_list[iterable], screen_width, screen_height, self.planet.rect.centerx, self.planet.rect.centery) \
		  		for iterable in range(len(meteors_sprite_list))]		

		# Players
		self.player_one = Player("Player1", variables.player_speed, variables.player_assets["Player1"],
			   						variables.player_running_assets["Player1"], self.planet.radius,
			   						(self.planet.rect.centerx,
									self.planet.rect.centery)
								)
		self.player_two = Player("Player2", variables.player_speed, variables.player_assets["Player2"],
			   						variables.player_running_assets["Player2"], self.planet.radius,
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

		self.font = pygame.font.Font(None, 120)

	def resetLevel(self):
		current_level = variables.current_level
		variables.game_data[current_level]["spaceship_one_hp"]["current"] = variables.game_data[current_level]["spaceship_one_hp"]["max"]
		variables.game_data[current_level]["spaceship_two_hp"]["current"] = variables.game_data[current_level]["spaceship_two_hp"]["max"]
		variables.game_data[current_level]["planet_hp"]["current"] = variables.game_data[current_level]["planet_hp"]["max"]
		variables.game_data[current_level]["initial_xp"]["current"] = 0
		variables.game_data[current_level]["asteroid_hp"]["current"] = variables.game_data[current_level]["asteroid_hp"]["max"]

	def handle_events(self):
		pass
		#for event in pygame.event.get():
			# if event.type == pygame.QUIT:
			# if one presses q key, the game quits
			#if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
			#	self.running = False
			#	pygame.quit()
			#	sys.exit()

	def start(self):
		self.running = True

	def pause(self):
		self.paused = not self.paused

	def restart(self):
		self.running = False
		self.paused = False
		#Variables Reset
		self.resetLevel()
		#Init the Level
		self.__init__(variables.screen_width, variables.screen_height, variables.fps, variables.current_level)
		self.start()
	
	def update_game_logic(self):
		if not self.paused:
			# Update game state
			self.asteroid.update()
			self.planet.update()

			# Check for game over collision between asteroid and the planet
			if pygame.sprite.collide_circle(self.asteroid, self.planet):
				self.game_over()
				self.saveLevelResult(condition="lose")
				return

			# Update both players
			self.player_one.update("Player1")
			self.player_two.update("Player2")

			current_level = variables.current_level

			# Check for collisions between players and spaceships, and handle interaction key presses
			for player, playerID in [(self.player_one, "Player1"), (self.player_two, "Player2")]:
				keys = pygame.key.get_pressed()
				if keys[variables.player_controls[playerID]["Interact"]["Use"]]:
					if player.in_spaceship is not None: # Player is in a spaceship and wants to leave
						aux_iterator = 0
						if not any(pygame.sprite.collide_circle(player, spaceship) for spaceship in [self.spaceship_one, self.spaceship_two]):
							# Only allow the player to leave the spaceship if they're not currently colliding with another one
							player.leave_spaceship(aux_iterator)
							player.respawn()
							aux_iterator = aux_iterator + 1
					else: # Player is not in a spaceship and wants to enter
						for spaceship in [self.spaceship_one, self.spaceship_two]:
							if pygame.sprite.collide_circle(player, spaceship):
								if spaceship.hp == variables.game_data[current_level]["spaceship_one_hp"]["max"] or spaceship.hp == variables.game_data[current_level]["spaceship_two_hp"]["max"]:
									player.enter_spaceship(spaceship, playerID)
									spaceship.reset_repair_counter()

								else:
									spaceship.repair()
									if spaceship == self.spaceship_one:
										variables.game_data[current_level]["spaceship_one_hp"]["current"] = spaceship.hp
									elif spaceship == self.spaceship_two:
										variables.game_data[current_level]["spaceship_two_hp"]["current"] = spaceship.hp
								break

			# Check for upgrade key
			if variables.game_data[current_level]["initial_xp"]['current'] >= variables.game_data[current_level]["initial_xp"]['max']: # Assuming 'u' is the upgrade key
				self.spaceship_one.upgrade(variables.spaceship_one_asset_upgrade)
				self.spaceship_two.upgrade(variables.spaceship_two_asset_upgrade)
					# for bullet in player.in_spaceship.bullets:
					# 	bullet.upgrade('path_to_new_bullet_sprite')  # Use the correct path to the new bullet sprite

			for meteor in self.meteors:
				meteor.update(speed=variables.game_data[variables.current_level]["meteor_speed"])
				# Check for collisions with the planet
				if pygame.sprite.collide_circle(meteor, self.planet):
					self.sound_player.playSoundEffect("meteor_impact_" + str(random.randint(1, 5)))
					meteor.respawn()
					variables.game_data[current_level]['planet_hp']['current'] -= variables.game_data[current_level]['planet_hp']['damage_per_hit']

				# Check for collisions between bullets and meteors/planet/asteroid
				for spaceship in [self.spaceship_one, self.spaceship_two]:
					for bullet in spaceship.bullets.copy():  # create a copy for iteration
						bullet_collided = False  # To keep track if bullet collided with any sprite

						# Check collision with each meteor
						for meteor in self.meteors:  # Assuming 'meteors' is a list of all meteors
							if pygame.sprite.collide_circle(meteor, bullet):
								self.sound_player.playSoundEffect("meteor_blast")
								bullet.remove()
								meteor.respawn()
								variables.game_data[current_level]['initial_xp']['current'] +=  variables.game_data[current_level]['initial_xp']['xp_per_hit']
								bullet_collided = True
								break  # Stop checking other meteors for this bullet

						# If bullet has not collided with any meteor, check for planet collision
						if not bullet_collided and pygame.sprite.collide_circle(self.planet, bullet):
							bullet.remove()
							bullet_collided = True

						# Check for asteroid collision, deal damage if spaceship is upgraded
						if not bullet_collided and pygame.sprite.collide_circle(self.asteroid, bullet):
							bullet.remove()
							bullet_collided = True
							if spaceship.upgraded:
								variables.game_data[current_level]['asteroid_hp']['current'] -= variables.game_data[current_level]['asteroid_hp']['damage_per_hit']

			# Update both spaceships and check for collisions with the asteroid
			for spaceship in [self.spaceship_one, self.spaceship_two]:
				aux_iterator = 0
				spaceship.update()
				if pygame.sprite.collide_circle(spaceship, self.asteroid):
					spaceship.reposition(aux_iterator)
					if(spaceship.playerID) == "Player1":
						self.player_one.leave_spaceship(0)
					elif(spaceship.playerID) == "Player2":
						self.player_two.leave_spaceship(1)
					if spaceship == self.spaceship_one:
						variables.game_data[current_level]["spaceship_one_hp"]['current'] = 0
						spaceship.hp = 0
					elif spaceship == self.spaceship_two:
						variables.game_data[current_level]["spaceship_two_hp"]['current'] = 0
						spaceship.hp = 0
				aux_iterator = aux_iterator + 1
			
			# Update UI
			self.ui.update()

			# Win Condition
			if variables.game_data[current_level]['asteroid_hp']['current'] <= 0:
				self.victory()
				self.saveLevelResult(condition="win")
				return

			# Lose Condition
			if variables.game_data[current_level]['planet_hp']['current'] <= 0:
				self.game_over()
				self.saveLevelResult(condition="lose")
				return


	def render(self):
		# Blit the background image to the screen
		self.screen.blit(self.background_image, (0, 0))
		
		# Draw UI
		self.ui.draw()

	def saveLevelResult(self,condition):
		if condition == "win":
			saveObject = SaveGame()			
			if variables.saved_game_data["last_completed_level"] == "None" \
				and self.button_level == "One":
				variables.saved_game_data["last_completed_level"] = "One"
				saveObject.save(variables.saved_game_data, variables.player_file)
				print("Game Saved! Level 2 unlocked!")

			elif variables.saved_game_data["last_completed_level"] == "One" \
				and self.button_level == "Two":
				variables.saved_game_data["last_completed_level"] = "Two"
				saveObject.save(variables.saved_game_data, variables.player_file)
				print("Game Saved! Level 3 unlocked!")

			elif variables.saved_game_data["last_completed_level"] == "Two" \
				and self.button_level == "Three":
				variables.saved_game_data["last_completed_level"] = "Three"
				saveObject.save(variables.saved_game_data, variables.player_file)
				print("Game Saved! You completed the game! Thanks for playing!")

			elif variables.saved_game_data["last_completed_level"] == "Three":
				pass
			else:
				print("Game Saved! No new level was unlocked!")
		elif condition == "lose":
			pass

		self.running = False
		self.resetLevel()

	def game_loop(self):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					pygame.quit()
					sys.exit()
					
				if event.type == pygame.KEYDOWN:
					if (event.key == variables.player_controls["Player1"]["Menu"]["Use"] or 
						event.key ==  variables.player_controls["Player2"]["Menu"]["Use"]):
						if not self.paused:
							#self.sound_player.pauseBackgroundMusic()  # Pause the current background music
							self.sound_player.stopBackgroundMusic()  # Stop the current background music
							self.pause_menu.sound_player.loadMenuBackgroundMusic(variables.pause_menu_music)
							self.pause_menu.sound_player.playBackgroundMusic()  # Start the pause menu music
							self.pause_menu.fade_in()
							self.paused = True  # Update the pause state
						elif self.paused:
							self.pause_menu.sound_player.stopBackgroundMusic()  # Stop the pause menu music
							if variables.current_level == "One":
								self.sound_player.loadBackgroundMusic(1, variables.background_music)
							elif variables.current_level == "Two":
								self.sound_player.loadBackgroundMusic(2, variables.background_music)
							else:
								print("Error: There was a problem loading the background music for the current level")
							#self.sound_player.unpauseBackgroundMusic()  # Resume the original background music
							self.sound_player.playBackgroundMusic()  # Start the pause menu music
							self.pause_menu.fade_out()
							self.paused = False  # Update the pause state
				
				if self.paused:
					pause_menu_action = self.pause_menu.handle_event(event)
					if pause_menu_action in [1, 2, 3]:  # If any action is performed, stop the pause menu music
						self.pause_menu.sound_player.stopBackgroundMusic()
					if pause_menu_action == 1:
						# Resume game
						self.paused = False
						if variables.current_level == "One":
							self.sound_player.loadBackgroundMusic(1, variables.background_music)
						elif variables.current_level == "Two":
							self.sound_player.loadBackgroundMusic(2, variables.background_music)
						else:
							print("Error: There was a problem loading the background music for the current level")
						#self.sound_player.unpauseBackgroundMusic()  # Resume the original background music
						self.sound_player.playBackgroundMusic()  # Start the pause menu music
					elif pause_menu_action == 2:
						# Restart game
						self.paused = False
						self.restart()  # Restart the level
					elif pause_menu_action == 3:
						# Go to main menu
						return
					continue
				else:
					self.handle_events()
			
			if not self.paused:
				self.update_game_logic()
				self.render()
			else:
				self.pause_menu.draw_menu()
			
			pygame.display.update()
			self.clock.tick(self.fps)

	def fade_in(self):
		fade_surface = pygame.Surface((variables.screen_width, variables.screen_height))  # Create new surface
		fade_surface.fill(variables.BLACK)  # Fill the surface with the desired color

		for alpha in range(0, 255, 25):  # Loop over alpha values, stepping by 25
			fade_surface.set_alpha(alpha)  # Set the alpha value
			self.render()  # Render your normal scene
			self.screen.blit(fade_surface, (0, 0))  # Blit the fade surface onto the screen
			pygame.display.update()  # Update the display
			pygame.time.delay(1)  # Pause for 1 millisecond to control the speed of the fade

	def victory(self):
		self.fade_in()
		self.sound_player.stopBackgroundMusic()  # Stop the current background music
		self.screen.fill(variables.BLACK)
		new_font = pygame.font.Font(None, 80)
		text = self.font.render("Victory!", True, variables.LIGHT_GREEN)
		text_continue = new_font.render("Press any Key to Continue!", True, variables.WHITE)
		text_rect = text.get_rect(center=(variables.screen_width/2, variables.screen_height/2))
		text_continue_rect = text_continue.get_rect(center=(variables.screen_width/2, variables.screen_height/2 +80))
		self.screen.blit(text, text_rect)
		self.screen.blit(text_continue, text_continue_rect)
		pygame.display.update()
		self.wait_for_key()

	def game_over(self):
		self.fade_in()
		self.sound_player.stopBackgroundMusic()  # Stop the current background music
		self.screen.fill(variables.BLACK)
		new_font = pygame.font.Font(None, 80)
		text = self.font.render("Game Over!", True, variables.RED)
		text_continue = new_font.render("Press any Key to Continue!", True, variables.WHITE)
		text_rect = text.get_rect(center=(variables.screen_width/2, variables.screen_height/2))
		text_continue_rect = text_continue.get_rect(center=(variables.screen_width/2, variables.screen_height/2 +80))
		self.screen.blit(text, text_rect)
		self.screen.blit(text_continue, text_continue_rect)
		pygame.display.update()
		self.wait_for_key()

	def wait_for_key(self):
		pygame.event.wait()  # wait for any event
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYUP:
					time.sleep(1)  # add delay
					return

class LevelOne(Level):
	def __init__(self, screen_width=None, screen_height=None, fps=variables.fps, button_level=None):
		super().__init__(screen_width, screen_height, fps)

		self.button_level = button_level

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
	def __init__(self, screen_width=None, screen_height=None, fps=variables.fps, button_level=None):
		super().__init__(screen_width, screen_height, fps)

		self.button_level = button_level

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

class LevelThree(Level):
	def __init__(self, screen_width=None, screen_height=None, fps=variables.fps, button_level=None):
		super().__init__(screen_width, screen_height, fps)

		self.button_level = button_level

		ast_sprite = pygame.image.load(os.path.join(cwd, variables.asteroid_asset))
		self.asteroid = Asteroid(ast_sprite, screen_width // 2, screen_height // 2)

		planet_sprite = pygame.image.load(os.path.join(cwd, variables.planet_asset))
		self.planet = Planet(planet_sprite, screen_width // 2, screen_height // 2)

		# Other Level 3 specific initialization...
		self.sound_player.loadBackgroundMusic(3,variables.background_music)

	def start(self):
		super().start()
		print("Level 3 Initialized")
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

class Game:
	def __init__(self, screen_width=None, screen_height=None, fps=variables.fps, button=None):
		self.current_level = button
		if self.current_level == "One":
			variables.current_level = "One"
			self.current_level = LevelOne(screen_width, screen_height, fps, button_level=self.current_level)  # Starts Level One
		elif self.current_level == "Two":
			variables.current_level = "Two"
			self.current_level = LevelTwo(screen_width, screen_height, fps, button_level=self.current_level)  # Starts Level Two
		elif self.current_level == "Three":
			variables.current_level = "Three"
			self.current_level = LevelThree(screen_width, screen_height, fps, button_level=self.current_level)  # Starts Level Three
		else:
			print("Invalid level name")
			pygame.quit()
			sys.exit()

	def start(self):
		self.current_level.start()