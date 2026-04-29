# db.py
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import json
import os

class Database:
    def __init__(self):
        self.use_postgres = False
        self.data_file = 'game_data.json'
        
        # Try to connect to PostgreSQL
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="postgres",  # Try to connect to default database first
                user="postgres",
                password="postgres",  # Default password, change if needed
                port="5432"
            )
            self.use_postgres = True
            self.create_tables()
            print("Connected to PostgreSQL database")
        except Exception as e:
            print(f"PostgreSQL connection failed: {e}")
            print("Using file-based storage instead")
            self.init_file_storage()
            
    def init_file_storage(self):
        """Initialize file-based storage as fallback"""
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump({"players": {}, "game_sessions": []}, f)
                
    def load_data(self):
        """Load data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except:
            return {"players": {}, "game_sessions": []}
            
    def save_data(self, data):
        """Save data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def create_tables(self):
        """Create PostgreSQL tables if they don't exist"""
        if not self.use_postgres:
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id),
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT NOW()
                )
            """)
            self.conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Error creating tables: {e}")
            self.use_postgres = False
            
    def get_or_create_player(self, username):
        """Get or create player ID"""
        if self.use_postgres:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
                result = cursor.fetchone()
                
                if result:
                    player_id = result[0]
                else:
                    cursor.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
                    player_id = cursor.fetchone()[0]
                    self.conn.commit()
                    
                cursor.close()
                return player_id
            except Exception as e:
                print(f"Error in get_or_create_player: {e}")
                self.use_postgres = False
        
        # File-based fallback
        data = self.load_data()
        if username not in data["players"]:
            data["players"][username] = len(data["players"]) + 1
            self.save_data(data)
        return data["players"][username]
        
    def save_game_result(self, username, score, level_reached):
        """Save game result to database"""
        try:
            player_id = self.get_or_create_player(username)
            
            if self.use_postgres:
                cursor = self.conn.cursor()
                cursor.execute("""
                    INSERT INTO game_sessions (player_id, score, level_reached)
                    VALUES (%s, %s, %s)
                """, (player_id, score, level_reached))
                self.conn.commit()
                cursor.close()
            else:
                # File-based storage
                data = self.load_data()
                data["game_sessions"].append({
                    "username": username,
                    "score": score,
                    "level_reached": level_reached,
                    "played_at": datetime.now().isoformat()
                })
                self.save_data(data)
            return True
        except Exception as e:
            print(f"Error saving game result: {e}")
            return False
            
    def get_leaderboard(self, limit=10):
        """Get top 10 scores"""
        try:
            if self.use_postgres:
                cursor = self.conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT p.username, gs.score, gs.level_reached, gs.played_at
                    FROM game_sessions gs
                    JOIN players p ON gs.player_id = p.id
                    ORDER BY gs.score DESC
                    LIMIT %s
                """, (limit,))
                results = cursor.fetchall()
                cursor.close()
                return results
            else:
                # File-based storage
                data = self.load_data()
                sessions = data["game_sessions"]
                # Sort by score descending
                sessions.sort(key=lambda x: x["score"], reverse=True)
                # Return top 'limit' results
                return [{
                    "username": s["username"],
                    "score": s["score"],
                    "level_reached": s["level_reached"],
                    "played_at": s["played_at"]
                } for s in sessions[:limit]]
        except Exception as e:
            print(f"Error getting leaderboard: {e}")
            return []
            
    def get_personal_best(self, username):
        """Get personal best score for a user"""
        try:
            if self.use_postgres:
                player_id = self.get_or_create_player(username)
                cursor = self.conn.cursor()
                cursor.execute("""
                    SELECT MAX(score) as best_score
                    FROM game_sessions
                    WHERE player_id = %s
                """, (player_id,))
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result and result[0] else 0
            else:
                # File-based storage
                data = self.load_data()
                best_score = 0
                for session in data["game_sessions"]:
                    if session["username"] == username and session["score"] > best_score:
                        best_score = session["score"]
                return best_score
        except Exception as e:
            print(f"Error getting personal best: {e}")
            return 0