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

		self.current_music = None  # Add a variable to hold the current music
		self.is_playing = False  # Add a variable to hold the playing state

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
		self.is_playing = True  # Update the playing state

	def setMusicVolume(self, volume_slider, music_volume):
		self.music_volume = volume_slider * music_volume
		pygame.mixer.music.set_volume(self.music_volume)

	def playAnotherBackgroundMusic(self, music_path):
		pygame.mixer.music.load(music_path)  # Load the new music
		pygame.mixer.music.play(-1)  # Start playing the new music
		self.current_music = music_path  # Save the current music
		self.is_playing = True  # Update the playing state

	def resumeBackgroundMusic(self):
		if self.current_music is not None:  # If a current music is saved
			pygame.mixer.music.unpause()  # Resume the saved music

	def stopBackgroundMusic(self):
		pygame.mixer.music.stop()
		self.is_playing = False  # Update the playing state

	def isMusicPlaying(self):
		return self.is_playing  # Return the current playing state

	def pauseBackgroundMusic(self):
		pygame.mixer.music.pause()

	def unpauseBackgroundMusic(self):
		pygame.mixer.music.unpause()

	def playSoundEffect(self, name):
		self.sound_volume = variables.global_sound_volume
		if name in self.sounds:
			self.sounds[name].play()
			self.sounds[name].set_volume(variables.sounds_volume[name] * variables.saved_game_data["sound_effect_slider"])
		else:
			print(f"Sound {name} not found!")
