# main.py - полностью рабочая версия
import pygame
import sys
import json
import os
import random
from datetime import datetime

def load_settings():
    default = {'snake_color': [0,255,0], 'grid': True, 'sound': True}
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r') as f:
                data = json.load(f)
                for k in default:
                    if k not in data:
                        data[k] = default[k]
                return data
        except:
            pass
    with open('settings.json', 'w') as f:
        json.dump(default, f)
    return default

class Database:
    def __init__(self):
        self.file = 'game_data.json'
        # Правильная инициализация файла
        if not os.path.exists(self.file):
            with open(self.file, 'w') as f:
                json.dump({"sessions": []}, f)
    
    def save_result(self, username, score, level):
        try:
            with open(self.file, 'r') as f:
                data = json.load(f)
        except:
            data = {"sessions": []}
    
        if "sessions" not in data:
            data["sessions"] = []
        
        data['sessions'].append({
            'username': username, 
            'score': score, 
            'level': level, 
            'date': datetime.now().strftime('%Y-%m-%d')
        })
        
        with open(self.file, 'w') as f:
            json.dump(data, f)
    
    def get_leaderboard(self):
        try:
            with open(self.file, 'r') as f:
                data = json.load(f)
        except:
            return []
        
        if "sessions" not in data:
            return []
        
        sorted_sessions = sorted(data['sessions'], key=lambda x: x['score'], reverse=True)
        return sorted_sessions[:10]
    
    def get_best(self, username):
        try:
            with open(self.file, 'r') as f:
                data = json.load(f)
        except:
            return 0
        
        if "sessions" not in data:
            return 0
        
        scores = [s['score'] for s in data['sessions'] if s['username'] == username]
        return max(scores) if scores else 0

class Button:
    def __init__(self, x, y, w, h, text, color, hover):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover = hover
        self.hovered = False
    
    def draw(self, screen, font):
        color = self.hover if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)
        text = font.render(self.text, True, (255,255,255))
        screen.blit(text, text.get_rect(center=self.rect.center))
    
    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        return event.type == pygame.MOUSEBUTTONDOWN and self.hovered

class Snake:
    def __init__(self, color):
        self.body = [[400,300]]
        self.dir = [20,0]
        self.color = color
        self.grow_flag = False
    
    def move(self):
        head = [self.body[0][0] + self.dir[0], self.body[0][1] + self.dir[1]]
        self.body.insert(0, head)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
    
    def grow(self):
        self.grow_flag = True
    
    def shrink(self):
        if len(self.body) > 2:
            self.body.pop()
            self.body.pop()
            return True
        return False
    
    def collide(self, w, h, obstacles):
        head = self.body[0]
        if head[0] < 0 or head[0] >= w or head[1] < 0 or head[1] >= h:
            return True
        if head in self.body[1:]:
            return True
        if head in obstacles:
            return True
        return False
    
    def change_dir(self, new):
        if [new[0]*-1, new[1]*-1] != self.dir:
            self.dir = new

class Item:
    def __init__(self, w, h, cell, color, obstacles):
        self.w, self.h, self.cell = w, h, cell
        self.color = color
        self.pos = self.random_pos(obstacles)
    
    def random_pos(self, obstacles):
        while True:
            x = random.randint(0, self.w//self.cell - 1) * self.cell
            y = random.randint(0, self.h//self.cell - 1) * self.cell
            if [x,y] not in obstacles:
                return [x,y]
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.pos, self.cell, self.cell))

class Game:
    def __init__(self, screen, db, username, settings):
        self.screen = screen
        self.db = db
        self.username = username
        self.settings = settings
        
        self.cell = 20
        self.w, self.h = 800, 600
        
        # НАСТРОЙКИ СКОРОСТИ
        self.move_delay = 150  # начальная задержка (мс)
        self.last_move_time = 0
        
        self.score = 0
        self.level = 1
        self.food_count = 0
        self.obstacles = []
        
        self.snake = Snake(settings['snake_color'])
        self.food = Item(self.w, self.h, self.cell, (255,0,0), self.obstacles)
        self.poison = None
        self.powerup = None
        self.active = {}
        
        self.game_over = False
        self.best = db.get_best(username)
        
        self.generate_obstacles()
    
    def random_pos(self):
        attempts = 0
        while attempts < 100:
            x = random.randint(0, self.w//self.cell - 1) * self.cell
            y = random.randint(0, self.h//self.cell - 1) * self.cell
            pos = [x,y]
            if pos not in self.snake.body and pos != self.food.pos and pos not in self.obstacles:
                return pos
            attempts += 1
        return [400, 300]
    
    def generate_obstacles(self):
        if self.level >= 3:
            count = min(5 + self.level, 15)
            self.obstacles = []
            attempts = 0
            while len(self.obstacles) < count and attempts < 100:
                x = random.randint(0, self.w//self.cell - 1) * self.cell
                y = random.randint(0, self.h//self.cell - 1) * self.cell
                pos = [x,y]
                if pos not in self.snake.body and pos != self.food.pos and pos not in self.obstacles:
                    self.obstacles.append(pos)
                attempts += 1
    
    def update(self):
        if self.game_over:
            return
        
        now = pygame.time.get_ticks()
        
        # Расчет текущей задержки с учетом бонусов
        current_delay = self.move_delay
        if self.active.get('speed_end', 0) > now:
            current_delay = int(self.move_delay * 0.7)
        if self.active.get('slow_end', 0) > now:
            current_delay = int(self.move_delay * 1.5)
        
        # Движение только по таймеру
        if now - self.last_move_time >= current_delay:
            self.last_move_time = now
            
            # Спавн предметов
            if not self.poison and random.random() < 0.02:
                self.poison = Item(self.w, self.h, self.cell, (139,0,0), self.obstacles + self.snake.body)
            
            if not self.powerup and random.random() < 0.01:
                types = ['speed', 'slow', 'shield']
                self.powerup = {'pos': self.random_pos(), 'type': random.choice(types), 'spawn': now}
            
            if self.powerup and now - self.powerup['spawn'] > 8000:
                self.powerup = None
            
            # Движение
            self.snake.move()
            
            # Проверка столкновений
            if self.snake.collide(self.w, self.h, self.obstacles):
                if self.active.get('shield_end', 0) > now:
                    self.active.pop('shield_end', None)
                    self.snake.body.pop(0)
                    self.snake.body.insert(0, [self.snake.body[0][0] - self.snake.dir[0], 
                                              self.snake.body[0][1] - self.snake.dir[1]])
                else:
                    self.end_game()
                    return
            
            # Поедание еды
            if self.snake.body[0] == self.food.pos:
                self.snake.grow()
                self.score += 10
                self.food_count += 1
                self.food = Item(self.w, self.h, self.cell, (255,0,0), self.obstacles + self.snake.body)
                
                if self.food_count % 5 == 0:
                    self.level += 1
                    self.move_delay = max(80, 150 - (self.level * 5))
                    self.generate_obstacles()
            
            # Поедание яда
            if self.poison and self.snake.body[0] == self.poison.pos:
                if not self.snake.shrink():
                    self.end_game()
                    return
                self.score = max(0, self.score - 5)
                self.poison = None
            
            # Поедание бонуса
            if self.powerup and self.snake.body[0] == self.powerup['pos']:
                t = self.powerup['type']
                if t == 'speed':
                    self.active['speed_end'] = now + 5000
                elif t == 'slow':
                    self.active['slow_end'] = now + 5000
                elif t == 'shield':
                    self.active['shield_end'] = now + 5000
                self.powerup = None
    
    def end_game(self):
        self.game_over = True
        self.db.save_result(self.username, self.score, self.level)
    
    def draw(self):
        self.screen.fill((0,0,0))
        
        # Препятствия
        for o in self.obstacles:
            pygame.draw.rect(self.screen, (100,100,100), (*o, self.cell, self.cell))
        
        # Змейка
        for seg in self.snake.body:
            pygame.draw.rect(self.screen, self.snake.color, (*seg, self.cell, self.cell))
        
        # Еда
        self.food.draw(self.screen)
        
        # Яд
        if self.poison:
            self.poison.draw(self.screen)
        
        # Бонус
        if self.powerup:
            colors = {'speed': (0,255,255), 'slow': (255,255,0), 'shield': (0,0,255)}
            pygame.draw.rect(self.screen, colors[self.powerup['type']], (*self.powerup['pos'], self.cell, self.cell))
        
        # Сетка
        if self.settings['grid']:
            for x in range(0, self.w, self.cell):
                pygame.draw.line(self.screen, (40,40,40), (x,0), (x,self.h))
            for y in range(0, self.h, self.cell):
                pygame.draw.line(self.screen, (40,40,40), (0,y), (self.w,y))
        
        # UI
        font = pygame.font.Font(None, 36)
        self.screen.blit(font.render(f"Score: {self.score}", True, (255,255,255)), (10,10))
        self.screen.blit(font.render(f"Level: {self.level}", True, (255,255,255)), (10,50))
        self.screen.blit(font.render(f"Best: {self.best}", True, (255,255,0)), (10,90))
        
        # Активные бонусы
        now = pygame.time.get_ticks()
        y = 130
        for key, end in self.active.items():
            if end > now:
                names = {'speed_end':'Speed', 'slow_end':'Slow', 'shield_end':'Shield'}
                text = font.render(f"{names[key]}: {(end-now)//1000}s", True, (0,255,255))
                self.screen.blit(text, (10,y))
                y += 35
    
    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.change_dir([0, -20])
            elif event.key == pygame.K_DOWN:
                self.snake.change_dir([0, 20])
            elif event.key == pygame.K_LEFT:
                self.snake.change_dir([-20, 0])
            elif event.key == pygame.K_RIGHT:
                self.snake.change_dir([20, 0])
            elif event.key == pygame.K_ESCAPE:
                return 'quit'
        return 'game_over' if self.game_over else None
class Screen:
    def __init__(self, screen, font, db=None):
        self.screen = screen
        self.font = font
        self.db = db
        self.cx = screen.get_width() // 2
    
    def draw_text(self, text, y, color=(255,255,255), size=36):
        font = pygame.font.Font(None, size)
        text = font.render(text, True, color)
        rect = text.get_rect(center=(self.cx, y))
        self.screen.blit(text, rect)

# Главное меню
class MenuScreen(Screen):
    def __init__(self, screen, font, db):
        super().__init__(screen, font, db)
        self.username = ""
        self.active = True
        
        y = 280
        self.buttons = {
            'play': Button(self.cx-100, y, 200, 50, "Play", (0,150,0), (0,200,0)),
            'leaderboard': Button(self.cx-100, y+70, 200, 50, "Leaderboard", (0,0,150), (0,0,200)),
            'settings': Button(self.cx-100, y+140, 200, 50, "Settings", (150,150,0), (200,200,0)),
            'quit': Button(self.cx-100, y+210, 200, 50, "Quit", (150,0,0), (200,0,0))
        }
    
    def draw(self):
        self.screen.fill((0,0,0))
        self.draw_text("SNAKE GAME", 80, (255,255,0), 60)

        box = pygame.Rect(self.cx-150, 170, 300, 50)
        pygame.draw.rect(self.screen, (50,50,50), box)
        pygame.draw.rect(self.screen, (255,255,255), box, 2)
        
        text = self.font.render(f"USERNAME: {self.username}", True, (255,255,255))
        self.screen.blit(text, (box.x+10, box.y+12))
        
        # Кнопки
        for btn in self.buttons.values():
            btn.draw(self.screen, self.font)
    
    def handle(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                if self.username:
                    self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            elif len(self.username) < 20 and event.unicode.isalnum():
                self.username += event.unicode
        
        for key, btn in self.buttons.items():
            if btn.handle(event):
                return key
        return None

class LeaderboardScreen(Screen):
    def __init__(self, screen, font, db):
        super().__init__(screen, font, db)
        self.back = Button(self.cx-100, 520, 200, 50, "Back", (0,0,150), (0,0,200))
    
    def draw(self):
        self.screen.fill((0,0,0))
        self.draw_text("LEADERBOARD - TOP 10", 50, (255,255,0), 50)
        
        data = self.db.get_leaderboard()
        
        headers = ["#", "Name", "Score", "Lvl", "Date"]
        xs = [50, 150, 350, 450, 550]
        
        for i, h in enumerate(headers):
            text = self.font.render(h, True, (255,255,255))
            self.screen.blit(text, (xs[i], 120))
        
        # Данные
        y = 170
        for i, entry in enumerate(data, 1):
            self.screen.blit(self.font.render(str(i), True, (200,200,200)), (xs[0], y))
            self.screen.blit(self.font.render(entry['username'][:12], True, (200,200,200)), (xs[1], y))
            self.screen.blit(self.font.render(str(entry['score']), True, (200,200,200)), (xs[2], y))
            self.screen.blit(self.font.render(str(entry['level']), True, (200,200,200)), (xs[3], y))
            self.screen.blit(self.font.render(entry['date'], True, (200,200,200)), (xs[4], y))
            y += 35
            if y > 480:
                break
        
        self.back.draw(self.screen, self.font)
    
    def handle(self, event):
        if self.back.handle(event):
            return 'back'
        return None

class SettingsScreen(Screen):
    def __init__(self, screen, font):
        super().__init__(screen, font)
        self.settings = load_settings()
        
        # Два цвета
        self.colors = [(0,255,0), (255,0,0)]  
        self.color_index = 0 if self.settings['snake_color'] == [0,255,0] else 1
        
        # Кнопки
        self.grid_btn = Button(self.cx-150, 250, 300, 50, 
                              f"Grid: {'ON' if self.settings['grid'] else 'OFF'}", 
                              (100,100,100), (150,150,150))
        self.save_btn = Button(self.cx-210, 450, 180, 50, "Save", (0,150,0), (0,200,0))
        self.back_btn = Button(self.cx+30, 450, 180, 50, "Back", (0,0,150), (0,0,200))
        
        # Для кнопок выбора цвета
        self.left_clicked = False
        self.right_clicked = False
    
    def draw(self):
        self.screen.fill((0,0,0))
        self.draw_text("SETTINGS", 50, (255,255,0), 60)
        
        # Цвет змеи
        self.draw_text("Snake Color:", 180, (255,255,255), 35)
        
        # Показываем текущий цвет
        color_rect = pygame.Rect(self.cx-40, 220, 80, 80)
        pygame.draw.rect(self.screen, self.colors[self.color_index], color_rect)
        pygame.draw.rect(self.screen, (255,255,255), color_rect, 3)
        
        # Название цвета
        color_name = "GREEN" if self.color_index == 0 else "RED"
        self.draw_text(color_name, 320, (255,255,0), 25)
        
        # Кнопки выбора цвета
        left_rect = pygame.Rect(self.cx-120, 240, 50, 40)
        right_rect = pygame.Rect(self.cx+80, 240, 50, 40)
        
        pygame.draw.rect(self.screen, (100,100,100), left_rect)
        pygame.draw.rect(self.screen, (100,100,100), right_rect)
        pygame.draw.rect(self.screen, (255,255,255), left_rect, 2)
        pygame.draw.rect(self.screen, (255,255,255), right_rect, 2)
        
        left_text = self.font.render("<", True, (255,255,255))
        right_text = self.font.render(">", True, (255,255,255))
        self.screen.blit(left_text, left_text.get_rect(center=left_rect.center))
        self.screen.blit(right_text, right_text.get_rect(center=right_rect.center))
        
        self.grid_btn.draw(self.screen, self.font)
        
        self.save_btn.draw(self.screen, self.font)
        self.back_btn.draw(self.screen, self.font)
    
        mouse = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        
        if mouse[0]:  
            if left_rect.collidepoint(pos) and not self.left_clicked:
                self.color_index = 0
                self.left_clicked = True
            elif right_rect.collidepoint(pos) and not self.right_clicked:
                self.color_index = 1
                self.right_clicked = True
        else:
            self.left_clicked = False
            self.right_clicked = False
    
    def handle(self, event):
        self.settings['snake_color'] = list(self.colors[self.color_index])
        
        #Grid
        if self.grid_btn.handle(event):
            self.settings['grid'] = not self.settings['grid']
            self.grid_btn.text = f"Grid: {'ON' if self.settings['grid'] else 'OFF'}"
        
        #button Save
        if self.save_btn.handle(event):
            with open('settings.json', 'w') as f:
                json.dump(self.settings, f)
            return 'save'
        
        # Back
        if self.back_btn.handle(event):
            return 'save'
        
        return None
class GameOverScreen(Screen):
    def __init__(self, screen, font, db, username, score, level, best):
        super().__init__(screen, font, db)
        self.username = username
        self.score = score
        self.level = level
        self.best = best
        
        self.retry = Button(self.cx-210, 400, 200, 50, "Retry", (0,150,0), (0,200,0))
        self.menu = Button(self.cx+10, 400, 200, 50, "Main Menu", (0,0,150), (0,0,200))
    
    def draw(self):
        self.screen.fill((0,0,0))
        self.draw_text("GAME OVER", 80, (255,0,0), 60)
        self.draw_text(f"Score: {self.score}", 180)
        self.draw_text(f"Level: {self.level}", 240)
        self.draw_text(f"Personal Best: {self.best}", 300, (255,255,0))
        self.retry.draw(self.screen, self.font)
        self.menu.draw(self.screen, self.font)
    
    def handle(self, event):
        if self.retry.handle(event):
            return 'retry'
        if self.menu.handle(event):
            return 'menu'
        return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    db = Database()
    settings = load_settings()
    
    menu = MenuScreen(screen, font, db)
    leaderboard = LeaderboardScreen(screen, font, db)
    settings_screen = SettingsScreen(screen, font)
    
    game = None
    game_over = None
    
    state = "menu"
    username = ""
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if state == "menu":
                result = menu.handle(event)
                if result == 'play' and menu.username:
                    username = menu.username
                    game = Game(screen, db, username, settings_screen.settings)
                    state = "game"
                elif result == 'leaderboard':
                    state = "leaderboard"
                elif result == 'settings':
                    state = "settings"
                elif result == 'quit':
                    running = False
            
            elif state == "game" and game:
                result = game.handle(event)
                if result == 'quit':
                    state = "menu"
                elif result == 'game_over':
                    game_over = GameOverScreen(screen, font, db, username, 
                                              game.score, game.level, game.best)
                    state = "game_over"
            
            elif state == "game_over" and game_over:
                result = game_over.handle(event)
                if result == 'retry':
                    game = Game(screen, db, username, settings_screen.settings)
                    state = "game"
                elif result == 'menu':
                    state = "menu"
            
            elif state == "leaderboard":
                if leaderboard.handle(event) == 'back':
                    state = "menu"
            
            elif state == "settings":
                if settings_screen.handle(event) == 'save':
                    state = "menu"
                    if game:
                        game.settings = settings_screen.settings
                        game.snake.color = tuple(settings_screen.settings['snake_color'])
        
        #rendering
        if state == "menu":
            menu.draw()
        elif state == "game" and game:
            game.update()
            game.draw()
        elif state == "game_over" and game_over:
            game_over.draw()
        elif state == "leaderboard":
            leaderboard.draw()
        elif state == "settings":
            settings_screen.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()