# game.py
import pygame
import random
import math
from datetime import datetime

class Snake:
    def __init__(self, start_pos, color):
        self.body = [start_pos]
        self.direction = (20, 0)
        self.color = color
        self.grow_flag = False
        
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
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
        else:
            return False
        return True
        
    def check_collision(self, width, height, obstacles=None):
        head = self.body[0]
        # Wall collision
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            return True
        # Self collision
        if head in self.body[1:]:
            return True
        # Obstacle collision
        if obstacles and head in obstacles:
            return True
        return False
        
    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

class Food:
    def __init__(self, width, height, cell_size, obstacles=None):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.obstacles = obstacles or []
        self.position = self.randomize_position()
        self.color = (255, 0, 0)
        
    def randomize_position(self):
        while True:
            x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
            y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
            if (x, y) not in self.obstacles:
                return (x, y)
                
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.cell_size, self.cell_size))

class PoisonFood(Food):
    def __init__(self, width, height, cell_size, obstacles=None):
        super().__init__(width, height, cell_size, obstacles)
        self.color = (139, 0, 0)  # Dark red
        
class PowerUp:
    def __init__(self, x, y, cell_size, type):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.type = type
        self.spawn_time = pygame.time.get_ticks()
        
        if type == "speed":
            self.color = (0, 255, 255)  # Cyan
        elif type == "slow":
            self.color = (255, 255, 0)  # Yellow
        elif type == "shield":
            self.color = (0, 255, 255)  # Blue
            
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.cell_size, self.cell_size))
        
    def is_expired(self, current_time):
        return current_time - self.spawn_time > 8000  # 8 seconds

class Game:
    def __init__(self, screen, clock, db, username, settings):
        self.screen = screen
        self.clock = clock
        self.db = db
        self.username = username
        self.settings = settings
        
        self.cell_size = 20
        self.width = 800
        self.height = 600
        self.speed = 10
        self.base_speed = 10
        
        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.obstacles = []
        
        # Get personal best
        self.personal_best = db.get_personal_best(username)
        
        # Initialize game objects
        snake_color = tuple(settings['snake_color'])
        start_pos = (self.width//2, self.height//2)
        self.snake = Snake(start_pos, snake_color)
        
        self.food = Food(self.width, self.height, self.cell_size, self.obstacles)
        self.poison_food = None
        self.power_up = None
        self.active_power_ups = {}  # {'shield': expiry_time}
        
        self.shield_active = False
        self.speed_boost_end = 0
        self.slow_motion_end = 0
        
        self.game_over = False
        
    def generate_obstacles(self):
        if self.level >= 3:
            num_obstacles = min(5 + self.level, 15)
            self.obstacles = []
            for _ in range(num_obstacles):
                while True:
                    x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
                    y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
                    pos = (x, y)
                    # Check if not trapping the snake
                    if pos not in self.snake.body and pos != self.food.position:
                        if self.poison_food and pos == self.poison_food.position:
                            continue
                        if self.power_up and pos == (self.power_up.x, self.power_up.y):
                            continue
                        self.obstacles.append(pos)
                        break
                        
    def spawn_power_up(self):
        if not self.power_up and random.random() < 0.01:  # 1% chance per frame
            types = ["speed", "slow", "shield"]
            power_type = random.choice(types)
            while True:
                x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
                y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
                pos = (x, y)
                if pos not in self.snake.body and pos != self.food.position and pos not in self.obstacles:
                    if self.poison_food and pos == self.poison_food.position:
                        continue
                    self.power_up = PowerUp(x, y, self.cell_size, power_type)
                    break
                    
    def spawn_poison_food(self):
        if not self.poison_food and random.random() < 0.005:  # 0.5% chance per frame
            self.poison_food = PoisonFood(self.width, self.height, self.cell_size, self.obstacles)
            
    def update_speed(self):
        current_time = pygame.time.get_ticks()
        speed = self.base_speed
        
        if self.speed_boost_end > current_time:
            speed = int(self.base_speed * 1.5)
        elif self.slow_motion_end > current_time:
            speed = int(self.base_speed * 0.5)
            
        self.speed = speed
        
    def update(self):
        if self.game_over:
            return
            
        current_time = pygame.time.get_ticks()
        
        # Update active power-ups
        self.update_speed()
        
        # Power-up expiry
        if self.power_up and self.power_up.is_expired(current_time):
            self.power_up = None
            
        # Spawn items
        self.spawn_power_up()
        self.spawn_poison_food()
        
        # Move snake
        self.snake.move()
        
        # Check game over conditions
        if self.snake.check_collision(self.width, self.height, self.obstacles):
            if self.shield_active and current_time < self.active_power_ups.get('shield', 0):
                self.shield_active = False
                # Revert the collision by moving back
                self.snake.body.pop(0)
                self.snake.body.insert(0, (self.snake.body[0][0] - self.snake.direction[0],
                                          self.snake.body[0][1] - self.snake.direction[1]))
            else:
                self.end_game()
                return
            
        # Check normal food collision
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.score += 10
            self.food_eaten += 1
            self.food = Food(self.width, self.height, self.cell_size, self.obstacles + self.snake.body)
            
            # Level up every 5 foods
            if self.food_eaten % 5 == 0:
                self.level += 1
                self.base_speed = min(10 + self.level, 25)
                self.generate_obstacles()
                
        # Check poison food collision
        if self.poison_food and self.snake.body[0] == self.poison_food.position:
            if not self.snake.shrink():
                self.end_game()
                return
            self.score = max(0, self.score - 5)
            self.poison_food = None
            
        # Check power-up collision
        if self.power_up and self.snake.body[0] == (self.power_up.x, self.power_up.y):
            if self.power_up.type == "speed":
                self.speed_boost_end = current_time + 5000
            elif self.power_up.type == "slow":
                self.slow_motion_end = current_time + 5000
            elif self.power_up.type == "shield":
                self.active_power_ups['shield'] = current_time + 5000
                self.shield_active = True
            self.power_up = None
            
    def draw_grid(self):
        if self.settings['grid']:
            for x in range(0, self.width, self.cell_size):
                pygame.draw.line(self.screen, (40,40,40), (x,0), (x,self.height))
            for y in range(0, self.height, self.cell_size):
                pygame.draw.line(self.screen, (40,40,40), (0,y), (self.width,y))
                
    def draw(self):
        self.screen.fill((0,0,0))
        
        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, (100,100,100), (obstacle[0], obstacle[1], self.cell_size, self.cell_size))
            
        # Draw snake
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, self.snake.color, (segment[0], segment[1], self.cell_size, self.cell_size))
            
        # Draw food
        self.food.draw(self.screen)
        
        # Draw poison food
        if self.poison_food:
            self.poison_food.draw(self.screen)
            
        # Draw power-up
        if self.power_up:
            self.power_up.draw(self.screen)
            
        # Draw grid
        self.draw_grid()
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255,255,255))
        level_text = font.render(f"Level: {self.level}", True, (255,255,255))
        best_text = font.render(f"Best: {self.personal_best}", True, (255,255,0))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        self.screen.blit(best_text, (10, 90))
        
        # Draw active power-ups
        current_time = pygame.time.get_ticks()
        y_offset = 130
        if self.speed_boost_end > current_time:
            remaining = (self.speed_boost_end - current_time) // 1000
            text = font.render(f"Speed Boost: {remaining}s", True, (0,255,255))
            self.screen.blit(text, (10, y_offset))
            y_offset += 40
        if self.slow_motion_end > current_time:
            remaining = (self.slow_motion_end - current_time) // 1000
            text = font.render(f"Slow Motion: {remaining}s", True, (255,255,0))
            self.screen.blit(text, (10, y_offset))
            y_offset += 40
        if self.active_power_ups.get('shield', 0) > current_time:
            remaining = (self.active_power_ups['shield'] - current_time) // 1000
            text = font.render(f"Shield: {remaining}s", True, (0,255,255))
            self.screen.blit(text, (10, y_offset))
            
    def end_game(self):
        self.game_over = True
        self.db.save_game_result(self.username, self.score, self.level)
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.change_direction((0, -self.cell_size))
            elif event.key == pygame.K_DOWN:
                self.snake.change_direction((0, self.cell_size))
            elif event.key == pygame.K_LEFT:
                self.snake.change_direction((-self.cell_size, 0))
            elif event.key == pygame.K_RIGHT:
                self.snake.change_direction((self.cell_size, 0))
            elif event.key == pygame.K_ESCAPE:
                return "quit"
                
        if self.game_over:
            return "game_over"
        return None