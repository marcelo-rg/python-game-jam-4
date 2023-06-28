import os
import pygame

####################
# Variables
####################

# Game Variables
game_name = "Asteroid Wasters"
screen_width = 800
screen_height = 600
fps = 60

####################

# Player Variables
player_speed = 1
spaceship_speed = 3

# Player Bindings
player_controls = { 
	"Player1": {
		"Move": {
			"Up": pygame.K_w,
			"Down": pygame.K_s,
			"Left": pygame.K_a,
			"Right": pygame.K_d
		},
		"Interact": {
			"Use": pygame.K_e
		},
		"Upgrade": {
			"Use": pygame.K_r
		},
		"Fire": {
			"Use": pygame.K_SPACE
		},
		"Menu": {
			"Use": pygame.K_ESCAPE
		}
	},
	"Player2": {
		"Move": {
			"Up": pygame.K_UP,
			"Down": pygame.K_DOWN,
			"Left": pygame.K_LEFT,
			"Right": pygame.K_RIGHT
		},
		"Interact": {
			"Use": pygame.K_j
		},
		"Upgrade": {
			"Use": pygame.K_k
		},
		"Fire": {
			"Use": pygame.K_l
		},
		"Menu": {
			"Use": pygame.K_p
		}
	}
}

####################

# Some colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

####################

# Paths
assets_path = "assets"
planet_assets_path = os.path.join(assets_path, "planet")
asteroid_assets_path = os.path.join(assets_path, "asteroid")
meteors_assets_path = os.path.join(assets_path, "meteors")
spaceships_assets_path = os.path.join(assets_path, "spaceships")
player_assets_path = os.path.join(assets_path, "player")
background_assets_path = os.path.join(assets_path, "background")
background_music_path = "music"
bullet_sprite_path = os.path.join(assets_path, "bullets","bullet1.png")
sound_path = os.path.join(assets_path, "..", "music")

####################

# Positions per Level
spaceship_positions  = {
	1: [(100, 100), (400, 200)],
	2: [(100, 100), (400, 200)]
}

player_assets_positions = {
	"Player1": {"x": 300, "y": 300},
	"Player2": {"x": 400, "y": 400}
}

####################

# Image Variables
background_image = os.path.join(background_assets_path, "space-galaxy-background.jpg")
asteroid_asset = os.path.join(asteroid_assets_path, "12-circular.png")
planet_asset = os.path.join(planet_assets_path, "14.png")
meteor_big_asset = os.path.join(meteors_assets_path,"meteorBrown_big")
spaceship_one_asset = os.path.join(spaceships_assets_path,"playerShip2_blue.png")
spaceship_two_asset = os.path.join(spaceships_assets_path,"playerShip2_green.png")
player_assets = {
	"Player1": os.path.join(player_assets_path, "player1.png"),
	"Player2": os.path.join(player_assets_path, "player2.png")
}

####################

# SPRITE SIZES
asteroid_sprite_size = 128
planet_sprite_size = 256
meteor_sprite_size = 32
bullet_sprite_size = (22,12)
spaceship_sprite_size  = {
	"no_upgrade": [(56, 38), (56, 38)],
	"upgrade_one": [(56, 38), (56, 38)]
}
player_assets_size = {
	"Player1": {"x": 32, "y": 32},
	"Player2": {"x": 32, "y": 32}
}

# This dictionary above has sprite size for both spaceships
# also it has a key 

####################

# Game Object Variables
spiral_radius = 400
spiral_speed = 0.005
spiral_decay_rate = 0.005
spaceship_rotation_speed = 2.0
bullet_speed = 6
bullet_cooldown = 20

####################

# Sound Variables
global_music_volume = 0.05
global_sound_volume = 0.05
italian_sound_volume = 0.5
background_music = "Itro-Tobu-Cloud-9.mp3"
sounds = {
    'shooting': os.path.join(sound_path, "shooting1.mp3"),
    'meteor_impact': os.path.join(sound_path, "Meteor1.mp3"),
}
sounds_volume = {
    'shooting': global_sound_volume,
    'meteor_impact': italian_sound_volume,
}
####################

# Exra Variables
jpg_extension = ".jpg"
png_extension = ".png"

####################

