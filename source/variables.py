import os

####################
# Variables
####################

# Game Variables
game_name = "Asteroid Wasters"
screen_width = 800
screen_height = 600
fps = 60

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
background_assets_path = os.path.join(assets_path, "background")
background_music_path = "music"

####################

# Image Variables
background_image = os.path.join(background_assets_path, "space-galaxy-background.jpg")
asteroid_asset = os.path.join(asteroid_assets_path, "12-circular.png")
planet_asset = os.path.join(planet_assets_path, "14.png")
meteor_big_asset = os.path.join(meteors_assets_path,"meteorBrown_big")

####################

# SPRITE SIZES
asteroid_sprite_size = 128
planet_sprite_size = 256
meteor_sprite_size = 32

####################

# Game Object Variables
spiral_radius = 400
spiral_speed = 0.005
spiral_decay_rate = 0.005

####################

# Sound Variables
global_volume = 0.0
background_music = "Itro-Tobu-Cloud-9.mp3"

####################

# Exra Variables
jpg_extension = ".jpg"
png_extension = ".png"

####################