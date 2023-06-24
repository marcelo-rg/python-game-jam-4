import os
import pygame

class MusicPlayer:
	####################
	# Variables
	####################
	# Path
	background_music_path = "music/"
	####################
	# Sound Variables
	background_music = "Itro-Tobu-Cloud-9.mp3"
	####################
	
	def __init__(self,volume=0.1):
		pygame.mixer.init()
		file_path = os.path.join(self.background_music_path, self.background_music)
		pygame.mixer.music.load(file_path)
		pygame.mixer.music.set_volume(volume)  # Set the volume

	def playBackgroundMusic(self):
		pygame.mixer.music.play(-1)  # -1 means loop indefinitely

	def stopBackgroundMusic(self):
		pygame.mixer.music.stop()
