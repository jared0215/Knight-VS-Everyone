import pygame


class MusicLoopComponent:
    def __init__(self, music_file):
        pygame.mixer.init()  # Initialize the mixer module
        self.music_file = music_file
        self.is_playing = False

    def play(self):
        if not self.is_playing:
            pygame.mixer.music.load(self.music_file)  # Load the music file
            pygame.mixer.music.play(-1)  # Play the music file in a loop
            self.is_playing = True

    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()  # Stop the music
            self.is_playing = False
