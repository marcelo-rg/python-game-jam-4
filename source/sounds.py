import os
import pygame
import variables

class SoundManager:
    def __init__(self, sounds):
        pygame.mixer.init()
        self.sounds = {name: pygame.mixer.Sound(path) for name, path in sounds.items()}
        self.music_volume = variables.global_music_volume
        self.sound_volume = variables.global_sound_volume

    def loadBackgroundMusic(self, path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)

    def playBackgroundMusic(self):
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    def stopBackgroundMusic(self):
        pygame.mixer.music.stop()

    def playSoundEffect(self, name):
        if name in self.sounds:
            self.sounds[name].play()
            self.sounds[name].set_volume(variables.sounds_volume[name])
        else:
            print(f"Sound {name} not found!")



