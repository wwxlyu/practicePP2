import pygame
import sys
import random
import os

from persistence import load_data, save_data
from racer import Player, Enemy
from ui import Button, CYAN, MAGENTA, DARK_BLUE, WHITE, YELLOW, GREEN, RED, GRAY, draw_gradient_background

class NeonRacer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((400, 600))
        pygame.display.set_caption("NEON RACER")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 52)
        
        base_path = os.path.dirname(__file__)
        self.set_path = os.path.join(base_path, 'settings.json')
        self.lead_path = os.path.join(base_path, 'leaderboard.json')

        # Load settings
        default_settings = {"sound": True, "color": "CYAN", "diff": 2}
        self.settings = load_data(self.set_path, default_settings)
        
        if "diff" not in self.settings:
            self.settings = default_settings
            save_data(self.set_path, self.settings)

        self.update_car_color()

        # Load sound
        try:
            self.crash_snd = pygame.mixer.Sound(os.path.join(base_path, "assets", "crash_sound.mp3"))
        except:
            self.crash_snd = None

    def update_car_color(self):
        self.car_color = CYAN if self.settings.get("color") == "CYAN" else MAGENTA

    def draw_text(self, text, font, color, x, y, center=False):
        surf = font.render(str(text), True, color)
        rect = surf.get_rect(center=(x, y) if center else (x, y))
        self.screen.blit(surf, rect)

    def menu(self):
        btns = [
            Button("START GAME", 100, 250, 200, 50, CYAN, "play"),
            Button("SCORES", 100, 320, 200, 50, CYAN, "scores"),
            Button("SETTINGS", 100, 390, 200, 50, CYAN, "settings"),
            Button("QUIT", 100, 460, 200, 50, RED, "quit")
        ]

        while True:
            draw_gradient_background(self.screen)
            
            # Title
            self.draw_text("RACER", self.font_large, MAGENTA, 200, 120, True)
            
            m_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for b in btns:
                        if b.is_clicked(m_pos):
                            if b.action_id == "play": self.play()
                            elif b.action_id == "scores": self.show_scores()
                            elif b.action_id == "settings": self.show_settings()
                            elif b.action_id == "quit": pygame.quit(); sys.exit()

            for b in btns:
                b.draw(self.screen, self.font_medium)
            
            # Controls hint
            self.draw_text("Use LEFT/RIGHT or A/D to move", self.font_small, GRAY, 200, 560, True)
            
            pygame.display.flip()
            self.clock.tick(60)

    def play(self):
        player = Player(self.car_color)
        enemies = pygame.sprite.Group()
        
        score = 0
        spawn_timer = 0
        
        running = True
        while running:
            draw_gradient_background(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            
            diff_level = self.settings.get("diff", 2)
            
            # Spawn enemies
            spawn_timer += 1
            spawn_delay = max(30, 60 - diff_level * 8)
            
            if spawn_timer > spawn_delay:
                enemy_speed = 2 + diff_level
                enemies.add(Enemy(enemy_speed))
                spawn_timer = 0
            
            # Update
            player.update()
            enemies.update()
            
            # Score - add points when enemies leave the screen
            for enemy in enemies:
                if enemy.rect.top > 600:
                    score += 10
                    enemy.kill()
                    print(f"Score: {score}")
            
            # Collision
            if pygame.sprite.spritecollide(player, enemies, False):
                if self.settings.get("sound") and self.crash_snd:
                    self.crash_snd.play()
                pygame.time.delay(500)
                self.game_over(score)
                return
            
            # Draw
            self.screen.blit(player.image, player.rect)
            enemies.draw(self.screen)
            
            # UI
            self.draw_text(f"SCORE: {score}", self.font_large, CYAN, 200, 50, True)
            self.draw_text(f"DIFFICULTY: {diff_level}", self.font_small, WHITE, 350, 580, True)
            
            pygame.display.flip()
            self.clock.tick(60)

    def game_over(self, score):
        # Get player name
        player_name = self.get_player_name(score)
        
        # Save to leaderboard
        leaderboard = load_data(self.lead_path, [])
        leaderboard.append({"name": player_name, "score": score})
        leaderboard = sorted(leaderboard, key=lambda x: x.get('score', 0), reverse=True)[:10]
        save_data(self.lead_path, leaderboard)
        
        back_btn = Button("MAIN MENU", 100, 450, 200, 50, CYAN, "back")
        
        while True:
            draw_gradient_background(self.screen)
            
            self.draw_text("GAME OVER", self.font_large, RED, 200, 150, True)
            self.draw_text(f"SCORE: {score}", self.font_medium, WHITE, 200, 250, True)
            
            m_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and back_btn.is_clicked(m_pos):
                    return
            
            back_btn.draw(self.screen, self.font_medium)
            pygame.display.flip()
            self.clock.tick(60)

    def get_player_name(self, score):
        name = ""
        entering = True
        
        while entering:
            draw_gradient_background(self.screen)
            
            self.draw_text("GAME OVER!", self.font_large, MAGENTA, 200, 100, True)
            self.draw_text(f"Your score: {score}", self.font_medium, CYAN, 200, 180, True)
            self.draw_text("Enter your name:", self.font_small, WHITE, 200, 250, True)
            
            # Input box
            input_rect = pygame.Rect(100, 280, 200, 40)
            pygame.draw.rect(self.screen, WHITE, input_rect, 2, border_radius=5)
            
            # Draw name
            name_surf = self.font_medium.render(name if name else "_", True, CYAN)
            self.screen.blit(name_surf, (input_rect.x + 10, input_rect.y + 8))
            
            self.draw_text("Press ENTER to save", self.font_small, GRAY, 200, 360, True)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) > 0:
                        return name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 15 and event.unicode.isprintable():
                            name += event.unicode
            
            pygame.display.flip()
            self.clock.tick(60)

    def show_settings(self):
        while True:
            draw_gradient_background(self.screen)
            self.draw_text("SETTINGS", self.font_large, CYAN, 200, 80, True)
            
            # Buttons
            color_btn = Button(f"CAR: {self.settings.get('color')}", 50, 180, 300, 50, WHITE, "color")
            sound_btn = Button(f"SOUND: {'ON' if self.settings.get('sound') else 'OFF'}", 50, 250, 300, 50, WHITE, "sound")
            diff_btn = Button(f"DIFFICULTY: {self.settings.get('diff')}", 50, 320, 300, 50, WHITE, "diff")
            back_btn = Button("BACK", 100, 450, 200, 50, MAGENTA, "back")
            
            # Difficulty info
            diff = self.settings.get('diff')
            if diff == 1:
                diff_text = "EASY - Slow enemies"
                diff_color = GREEN
            elif diff == 2:
                diff_text = "MEDIUM - Normal speed"
                diff_color = YELLOW
            else:
                diff_text = "HARD - Fast enemies"
                diff_color = RED
            
            self.draw_text(diff_text, self.font_small, diff_color, 200, 390, True)
            
            m_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if color_btn.is_clicked(m_pos):
                        self.settings["color"] = "MAGENTA" if self.settings["color"] == "CYAN" else "CYAN"
                        self.update_car_color()
                    elif sound_btn.is_clicked(m_pos):
                        self.settings["sound"] = not self.settings["sound"]
                    elif diff_btn.is_clicked(m_pos):
                        self.settings["diff"] = (self.settings["diff"] % 3) + 1
                    elif back_btn.is_clicked(m_pos):
                        save_data(self.set_path, self.settings)
                        return
            
            color_btn.draw(self.screen, self.font_medium)
            sound_btn.draw(self.screen, self.font_medium)
            diff_btn.draw(self.screen, self.font_medium)
            back_btn.draw(self.screen, self.font_medium)
            
            pygame.display.flip()
            self.clock.tick(60)

    def show_scores(self):
        back_btn = Button("BACK", 100, 520, 200, 50, CYAN, "back")
        
        while True:
            draw_gradient_background(self.screen)
            self.draw_text("TOP 10 RACERS", self.font_large, MAGENTA, 200, 50, True)
            
            leaderboard = load_data(self.lead_path, [])
            
            if not leaderboard:
                self.draw_text("No scores yet!", self.font_medium, WHITE, 200, 300, True)
            else:
                for i, entry in enumerate(leaderboard[:10]):
                    name = entry.get('name', 'PLAYER')
                    score_val = entry.get('score', 0)
                    
                    # Color for top 3
                    if i == 0:
                        color = YELLOW
                        prefix = "1st"
                    elif i == 1:
                        color = GRAY
                        prefix = "2nd"
                    elif i == 2:
                        color = (205, 127, 50)  # Bronze
                        prefix = "3rd"
                    else:
                        color = WHITE
                        prefix = f"{i+1}th"
                    
                    text = f"{prefix}. {name} - {score_val} pts"
                    self.draw_text(text, self.font_small, color, 70, 120 + i*35, False)
            
            m_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and back_btn.is_clicked(m_pos):
                    return
            
            back_btn.draw(self.screen, self.font_medium)
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = NeonRacer()
    game.menu()