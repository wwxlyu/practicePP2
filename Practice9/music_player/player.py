import pygame
import os

class MusicPlayer:
    def __init__(self, music_dir):
        pygame.mixer.init()
        self.music_dir = music_dir
        #Filtering only audio files
        self.playlist = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
        self.current_index = 0
        self.is_paused = False
        self.song_duration = 0

    def load_track(self):
        if not self.playlist:
            return
        
        path = os.path.join(self.music_dir, self.playlist[self.current_index])
        pygame.mixer.music.load(path)
        
        #Pre-load duration to avoid lag in the main loop
        temp_sound = pygame.mixer.Sound(path)
        self.song_duration = temp_sound.get_length()

    def play(self):
        if not self.playlist: return
        
        #If it was stopped or track changed, reload and play
        if not pygame.mixer.music.get_busy() and not self.is_paused:
            self.load_track()
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.unpause()
            
        self.is_paused = False

    def pause(self):
        pygame.mixer.music.pause()
        self.is_paused = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_paused = False

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.stop()
        self.play()

    def previous_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.stop()
        self.play()

    def get_info(self):
        if not self.playlist:
            return "No tracks found", "Status: Empty"
        
        status = "Paused" if self.is_paused else "Playing"
        if not pygame.mixer.music.get_busy() and not self.is_paused:
            status = "Stopped"
            
        return self.playlist[self.current_index], status