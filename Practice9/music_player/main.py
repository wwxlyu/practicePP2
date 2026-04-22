import pygame
import os
from player import MusicPlayer

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 350
FPS = 30

# Colors 
BG_COLOR = (255, 240, 245)     #Lavender Blush
CARD_COLOR = (255, 255, 255)   #White
ACCENT_COLOR = (255, 182, 193) #Light Pink
PROGRESS_COLOR = (255, 20, 147) #Deep Pink
TEXT_PRIMARY = (75, 0, 130)    #Indigo-ish for contrast

class AudioApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Player")
        self.clock = pygame.time.Clock()
        
        # Setup paths
        base_path = os.path.dirname(__file__)
        music_path = os.path.join(base_path, "music", "sample_tracks")
        self.player = MusicPlayer(music_path)
        
        self.title_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 14)
        
        self.running = True

    def format_timestamp(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def draw_interface(self):
        self.screen.fill(BG_COLOR)

        pygame.draw.rect(self.screen, CARD_COLOR, (40, 40, 420, 220), border_radius=15)
        
        #Fetching info
        track_name, status_label = self.player.get_info()
        
        #Drawing Song Icon
        pygame.draw.circle(self.screen, ACCENT_COLOR, (100, 100), 30)
        pygame.draw.rect(self.screen, TEXT_PRIMARY, (110, 80, 4, 30))
        
        #Text Rendering
        name_surf = self.title_font.render(track_name, True, TEXT_PRIMARY)
        self.screen.blit(name_surf, (150, 85))
        
        status_surf = self.small_font.render(status_label, True, PROGRESS_COLOR)
        self.screen.blit(status_surf, (150, 115))

        #Progress Bar Logic
        current_time = pygame.mixer.music.get_pos() / 1000 #Convert to seconds
        total_time = self.player.song_duration
        
        bar_rect = pygame.Rect(80, 180, 340, 6)
        pygame.draw.rect(self.screen, BG_COLOR, bar_rect, border_radius=3)
        
        if total_time > 0 and current_time >= 0:
            progress_width = min((current_time / total_time) * 340, 340)
            pygame.draw.rect(self.screen, PROGRESS_COLOR, (80, 180, progress_width, 6), border_radius=3)
            
            #Timestamps
            time_str = f"{self.format_timestamp(current_time)} / {self.format_timestamp(total_time)}"
            time_surf = self.small_font.render(time_str, True, TEXT_PRIMARY)
            self.screen.blit(time_surf, (SCREEN_WIDTH // 2 - time_surf.get_width() // 2, 200))

        #Bottom Hints
        hints = "P: Play | S: Stop | N: Next | B: Previous"
        hint_surf = self.small_font.render(hints, True, (150, 100, 120))
        self.screen.blit(hint_surf, (SCREEN_WIDTH // 2 - hint_surf.get_width() // 2, 300))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: self.player.play()
                    if event.key == pygame.K_s: self.player.stop()
                    if event.key == pygame.K_n: self.player.next_track()
                    if event.key == pygame.K_b: self.player.previous_track()

            self.draw_interface()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    app = AudioApp()
    app.run()