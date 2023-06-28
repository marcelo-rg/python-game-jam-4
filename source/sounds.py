import os
import pygame
import variables

class MusicPlayer:
	def __init__(self):
		pygame.mixer.init()
		# Using vars from variables.py
		file_path = os.path.join(variables.background_music_path, variables.background_music)
		pygame.mixer.music.load(file_path)
		# Using volume vars from variables.py
		pygame.mixer.music.set_volume(variables.global_music_volume)  # Set the volume

	def playBackgroundMusic(self):
		pygame.mixer.music.play(-1)  # -1 means loop indefinitely

	def stopBackgroundMusic(self):
		pygame.mixer.music.stop()
