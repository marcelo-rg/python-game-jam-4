import os
import pygame
import math

####################
# Variables
####################

# Game Variables
game_name = "Meteor Mayhem"
screen_width = 800
screen_height = 600
fps = 60
options_menu_name = "Options Menu"
level_selection_menu_name = "Select Level"
level_selection_info = "Complete one Level to unlock the next"

# Save Variables
key_file = "player.key"
player_file = "player.data"
saved_game_data = {
    'music_slider': 1,
    'sound_effect_slider': 1,
    'last_completed_level': "One"
}

####################

# Player Variables
player_speed = 1
spaceship_speed = 3

spaceship_one_hp = {
	"current": 100,
	"max": 100,
}
spaceship_two_hp = {
	"current": 100,
	"max": 100
}
planet_hp = {
	"current": 500,
	"max": 500,
    "damage_per_hit": 30
}
initial_xp = {
	"current": 0,
	"max": 1000,
    "xp_per_hit": 100
}

asteroid_hp = {
	"current": 100,
	"max": 100,
    "damage_per_hit": 10
}

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
			"Use": pygame.K_f
		},
		"Fire": {
			"Use": pygame.K_SPACE
		},
		"Menu": {
			"Use": pygame.K_ESCAPE
		},
	
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
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (200, 200, 0)
LIGHT_GREEN = (80, 200, 120)
ANOTHER_GREEN = (46, 139, 87)
DARK_GREEN_v1 = (21, 71, 52)
DARK_GREEN = (54, 143, 107)
DARKER_GREEN = (15, 50, 36)
BLUE = (0, 0, 255)
TITLE_COLOR = (219, 161, 15)

####################

# Paths
assets_path = "assets"
planet_assets_path = os.path.join(assets_path, "planet")
asteroid_assets_path = os.path.join(assets_path, "asteroid")
meteors_assets_path = os.path.join(assets_path, "meteors")
spaceships_assets_path = os.path.join(assets_path, "spaceships")
player_assets_path = os.path.join(assets_path, "player")
background_assets_path = os.path.join(assets_path, "background")
bullet_sprite_path = os.path.join(assets_path, "bullets","bullet1.png")
bullet_sprite_path_upgraded = os.path.join(assets_path, "bullets","bullet2.png")
sound_path = os.path.join(assets_path, "..", "music")
isolaproduction_path = os.path.join(sound_path, "isolaproduction")

####################

# Positions per Level
spaceship_position_angles  = {
	1: [math.pi/2, -math.pi/2],
}

player_assets_positions = {
	"Player1": {"x": 300, "y": 300},
	"Player2": {"x": 400, "y": 400}
}

####################

# Image Variables
menu_background_image = os.path.join(background_assets_path, "menu-background.jpg")
background_image = os.path.join(background_assets_path, "purple_light_cleanup.png")
asteroid_asset = os.path.join(asteroid_assets_path, "12-circular.png")
planet_asset = os.path.join(planet_assets_path, "14.png")
meteor_big_asset = os.path.join(meteors_assets_path,"meteorBrown_big")
spaceship_one_asset = os.path.join(spaceships_assets_path,"playerShip2_blue.png")
spaceship_two_asset = os.path.join(spaceships_assets_path,"playerShip2_green.png")
spaceship_one_asset_upgrade = os.path.join(spaceships_assets_path,"playerShip3_blue.png")
spaceship_two_asset_upgrade = os.path.join(spaceships_assets_path,"playerShip3_green.png")
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
	"Player1": {"x": 42, "y": 42},
	"Player2": {"x": 42, "y": 42}
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
global_music_volume = 0.3
global_sound_volume = 0.05
italian_sound_volume = 0.5
main_menu_music = "ThemeTRY1.mp3"
pause_menu_music = "ThemeTRY2.mp3"
background_music = {
    0: "Trying_to_go_home.wav",
	1: "Not_far_enough.wav",
	2: "Is_not_over.wav"
}

sounds = {
	"shooting": os.path.join(sound_path, "shooting1.mp3"),
    "meteor_blast": os.path.join(sound_path, "Explosion.wav"),
	"meteor_impact_1": os.path.join(sound_path, "Meteor1.mp3"),
	"meteor_impact_2": os.path.join(sound_path, "Meteor_2.wav"),
	"meteor_impact_3": os.path.join(sound_path, "Meteor_3.wav"),
	"meteor_impact_4": os.path.join(sound_path, "Meteor_4.wav"),
	"meteor_impact_5": os.path.join(sound_path, "Meteor_5.wav"),
	"play_button": os.path.join(isolaproduction_path, "1-Play_button.wav"),
	"option_button": os.path.join(isolaproduction_path, "2-Option_button.wav"),
    "quit_button": os.path.join(isolaproduction_path, "3-Quit_button.wav"),
    "click_button": os.path.join(isolaproduction_path, "4-Click_confirm.wav")
}
sounds_volume = {
	'shooting': global_sound_volume,
	'meteor_blast': italian_sound_volume,
	'meteor_impact_1': italian_sound_volume,
	'meteor_impact_2': italian_sound_volume,
	'meteor_impact_3': italian_sound_volume,
	'meteor_impact_4': italian_sound_volume,
	'meteor_impact_5': italian_sound_volume,
    "play_button": italian_sound_volume,
    "option_button": italian_sound_volume,
    "quit_button": italian_sound_volume,
    "click_button": italian_sound_volume
}

####################

# Exra Variables
jpg_extension = ".jpg"
png_extension = ".png"

####################

