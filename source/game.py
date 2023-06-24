import pygame
import os 
cwd = os.getcwd()


from objects import Planet, Asteroid

class Game:
	def __init__(self, screen_width = None, screen_height = None, fps= 60):
		# Initialize Pygame
		pygame.init()

		if screen_width is None or screen_height is None:
			# Get the screen size
			screen_info = pygame.display.Info()
			screen_width = screen_info.current_w
			screen_height = screen_info.current_h

		# Set up the game window
		self.screen = pygame.display.set_mode((screen_width, screen_height))
		pygame.display.set_caption("My Game")

		# Set up the game clock
		self.clock = pygame.time.Clock()
		self.fps = fps

		# Game state
		self.running = False 
		self.paused = False

		# Add game elements here
		ast_sprite = pygame.image.load(cwd + "\\assets\\asteroid\\12-circular.png")
		self.asteroid = Asteroid(ast_sprite, screen_width // 2, screen_height // 2)
		# asteroid_rect = self.planet.sprite.get_rect()
		# asteroid_x = (screen_width - asteroid_rect.width) // 2
		# asteroid_y = (screen_height - asteroid_rect.height) // 2
		# self.planet.position = pygame.Vector2(asteroid_x, asteroid_y)

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
				if event.key == pygame.K_p:
					self.pause()
				elif event.key == pygame.K_r:
					self.restart()
				elif event.key == pygame.K_w:
					print("Move the character forwards")
				elif event.key == pygame.K_s:
					print("Move the character backwards")
				elif event.key == pygame.K_a:
					print("Move the character left")
				elif event.key == pygame.K_d:
					print("Move the character right")
				elif event.key == pygame.K_q:
					self.running = False


	def update_game_logic(self):
		if not self.paused:
			# Update game state
			# keys_pressed = pygame.key.get_pressed()
			self.asteroid.update()

	def render(self):
		# Render the game elements
		self.screen.fill((0, 0, 0))  # Example background fill

		# Add your rendering code here
		self.asteroid.render(self.screen)

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
	game = Game(fps = 90)
	game.start()
