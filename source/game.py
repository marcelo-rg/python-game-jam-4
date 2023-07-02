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
	def __init__(self, x, y, w, h, text='', sound_manager=None, value=0, slider_type=''):
		self.rect = pygame.Rect(x, y, w, h)
		self.color = variables.DARK_GREEN
		self.txt_color = variables.WHITE
		self.fill_color = variables.LIGHT_GREEN  # New fill color
		#self.fill_color = variables.ANOTHER_GREEN  # New fill color
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
				#print("Music volume was changed to: " + str(self.value))
				variables.saved_game_data["music_slider"] = self.value
				self.sound_manager.setMusicVolume(variables.saved_game_data["music_slider"], variables.global_music_volume)
			elif self.slider_type == 'sfx' and old_value != self.value:  # Check if slider type is sfx and the value has changed
				#print("SFX volume was changed to: " + str(self.value))
				variables.saved_game_data["sound_effect_slider"] = self.value
			return True
		return False


class UI:
	def __init__(self, screen):
		self.screen = screen

		# Initialize sliders
		self.slider_p1 = Slider(0, 100, step, position)
		self.slider_p2 = Slider(0, 100, step, position)
		self.slider_planet = Slider(0, 600, step, position)
		self.slider_xp = Slider(start_value, end_value, step, position)

	def draw(self):
		# Draw each slider on the screen
		self.slider_p1.draw(self.screen)
		self.slider_p2.draw(self.screen)
		self.slider_planet.draw(self.screen)
		self.slider_xp.draw(self.screen)

	def update(self, p1_hp, p2_hp, planet_hp, xp):
		# Update slider values based on the current game state
		self.slider_p1.set_value(p1_hp)
		self.slider_p2.set_value(p2_hp)
		self.slider_planet.set_value(planet_hp)
		self.slider_xp.set_value(xp)

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


	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
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
		pass

	def render(self):
		# Blit the background image to the screen
		self.screen.blit(self.background_image, (0, 0))

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
