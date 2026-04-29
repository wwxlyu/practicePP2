
#Window / Grid 
CELL_SIZE   = 20          # pixels per grid cell
GRID_W      = 30          # cells horizontally
GRID_H      = 30          # cells vertically
SCREEN_W    = CELL_SIZE * GRID_W          # 600 px
SCREEN_H    = CELL_SIZE * GRID_H + 80    # extra 80 px for HUD bar
FPS         = 10          # base frames-per-second (speed increases with level)

#Colors
BLACK       = (  0,   0,   0)
WHITE       = (255, 255, 255)
GREEN       = ( 50, 205,  50)
DARK_GREEN  = ( 34, 139,  34)
RED         = (220,  20,  60)
DARK_RED    = (139,   0,   0)
ORANGE      = (255, 140,   0)
BLUE        = ( 30, 144, 255)
YELLOW      = (255, 215,   0)
GRAY        = (100, 100, 100)
LIGHT_GRAY  = (200, 200, 200)
DARK_GRAY   = ( 40,  40,  40)
PURPLE      = (148,   0, 211)
CYAN        = (  0, 255, 255)
BG_COLOR    = ( 15,  15,  15)

#Scoring
POINTS_NORMAL   = 10
POINTS_POISON   = -5   
POINTS_PER_LEVEL = 50  
SPEED_INCREMENT  = 1  

#Food / Poison
POISON_CHANCE       = 0.20   
POISON_SHRINK_CELLS = 2      

#Power-ups
POWERUP_SPAWN_CHANCE = 0.15         
POWERUP_TYPES = {
    "speed_boost":  {"color": CYAN,   "duration": 5,  "label": "SPEED+"},
    "slow_motion":  {"color": BLUE,   "duration": 7,  "label": "SLOW"},
    "shield":       {"color": PURPLE, "duration": 0,  "label": "SHIELD"},  
}

#Obstacles 
OBSTACLE_START_LEVEL = 5    
OBSTACLE_COUNT_BASE  = 3    

#Database 
DB_HOST     = "localhost"
DB_PORT     = 5432
DB_NAME     = "snake_db"
DB_USER     = "postgres"
DB_PASSWORD = "password"

#Settings file
SETTINGS_FILE = "settings.json"