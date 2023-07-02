import os
import pygame
import variables
import random

class SoundManager:
	def __init__(self, sounds):
		pygame.mixer.init()
		self.sounds = {name: pygame.mixer.Sound(path) for name, path in sounds.items()}
		self.music_volume = variables.global_music_volume * variables.saved_game_data["music_slider"]
		self.sound_volume = variables.global_sound_volume * variables.saved_game_data["sound_effect_slider"]

	def loadBackgroundMusic(self, level, music_dict):
		# Generate a random number between 1 and the size of the dictionary
		#random_number = random.randint(1, len(music_dict))

		# Select the music file based on the random number
		music_file = music_dict[level]
		
		pygame.mixer.music.load(os.path.join(variables.sound_path,music_file))
		pygame.mixer.music.set_volume(self.music_volume)
	
	def loadMenuBackgroundMusic(self, music_file):
		
		pygame.mixer.music.load(os.path.join(variables.isolaproduction_path,music_file))
		pygame.mixer.music.set_volume(self.music_volume)

	def playBackgroundMusic(self):
		pygame.mixer.music.play(-1)  # -1 means loop indefinitely

	def setMusicVolume(self, volume_slider, music_volume):
		self.music_volume = volume_slider * music_volume
		pygame.mixer.music.set_volume(self.music_volume)

	def stopBackgroundMusic(self):
		pygame.mixer.music.stop()

	def playSoundEffect(self, name):
		self.sound_volume = variables.global_sound_volume
		if name in self.sounds:
			self.sounds[name].play()
			self.sounds[name].set_volume(variables.sounds_volume[name] * variables.saved_game_data["sound_effect_slider"])
		else:
			print(f"Sound {name} not found!")
