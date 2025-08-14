import sqlite3
import logging
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database manager for Duel Lords tournament data"""
    
    def __init__(self, db_path="duel_lords.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_db_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database tables"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Players table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    discord_id TEXT UNIQUE NOT NULL,
                    username TEXT NOT NULL,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    draws INTEGER DEFAULT 0,
                    kills INTEGER DEFAULT 0,
                    deaths INTEGER DEFAULT 0,
                    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Matches table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player1_id INTEGER NOT NULL,
                    player2_id INTEGER NOT NULL,
                    scheduled_time TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'scheduled',
                    winner_id INTEGER,
                    player1_kills INTEGER DEFAULT 0,
                    player2_kills INTEGER DEFAULT 0,
                    notes TEXT,
                    reminder_sent BOOLEAN DEFAULT 0,
                    FOREIGN KEY (player1_id) REFERENCES players (id),
                    FOREIGN KEY (player2_id) REFERENCES players (id),
                    FOREIGN KEY (winner_id) REFERENCES players (id)
                )
            ''')
            
            # Tournaments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tournaments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    start_date TIMESTAMP NOT NULL,
                    end_date TIMESTAMP,
                    status TEXT DEFAULT 'upcoming',
                    max_players INTEGER DEFAULT 16,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    def register_player(self, discord_id: str, username: str):
        """Register a new player"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO players (discord_id, username) VALUES (?, ?)',
                    (discord_id, username)
                )
                conn.commit()
                logger.info(f"Player {username} registered successfully")
                return True, f"Player {username} registered successfully!"
        except sqlite3.IntegrityError:
            return False, "Player is already registered!"
        except Exception as e:
            logger.error(f"Error registering player: {e}")
            return False, f"Registration failed: {str(e)}"
    
    def remove_player(self, discord_id: str):
        """Remove a player from the tournament"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE players SET is_active = 0 WHERE discord_id = ?',
                    (discord_id,)
                )
                
                if cursor.rowcount == 0:
                    return False, "Player not found!"
                
                conn.commit()
                return True, "Player removed successfully!"
        except Exception as e:
            logger.error(f"Error removing player: {e}")
            return False, f"Removal failed: {str(e)}"
    
    def get_player(self, discord_id: str):
        """Get player information"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM players WHERE discord_id = ? AND is_active = 1',
                    (discord_id,)
                )
                row = cursor.fetchone()
                
                if row:
                    return dict(row)
                return None
        except Exception as e:
            logger.error(f"Error getting player: {e}")
            return None
    
    def get_all_players(self):
        """Get all active players"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM players WHERE is_active = 1 ORDER BY username'
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting all players: {e}")
            return []
    
    def get_leaderboard(self, limit=20):
        """Get leaderboard sorted by wins and kills"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM players 
                    WHERE is_active = 1 
                    ORDER BY wins DESC, kills DESC, (wins + losses + draws) DESC
                    LIMIT ?
                ''', (limit,))
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []
    
    def schedule_match(self, player1_discord_id: str, player2_discord_id: str, scheduled_time: datetime):
        """Schedule a match between two players"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Get player IDs
                cursor.execute('SELECT id FROM players WHERE discord_id = ? AND is_active = 1', (player1_discord_id,))
                player1_row = cursor.fetchone()
                if not player1_row:
                    return False, "Player 1 not found or inactive!"
                
                cursor.execute('SELECT id FROM players WHERE discord_id = ? AND is_active = 1', (player2_discord_id,))
                player2_row = cursor.fetchone()
                if not player2_row:
                    return False, "Player 2 not found or inactive!"
                
                player1_id = player1_row[0]
                player2_id = player2_row[0]
                
                # Insert match
                cursor.execute('''
                    INSERT INTO matches (player1_id, player2_id, scheduled_time)
                    VALUES (?, ?, ?)
                ''', (player1_id, player2_id, scheduled_time))
                
                match_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Match {match_id} scheduled successfully")
                return True, f"Match scheduled successfully! ID: {match_id}"
                
        except Exception as e:
            logger.error(f"Error scheduling match: {e}")
            return False, f"Scheduling failed: {str(e)}"
    
    def update_player_stats(self, discord_id: str, wins: int = 0, losses: int = 0, 
                           draws: int = 0, kills: int = 0, deaths: int = 0):
        """Update player statistics"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE players 
                    SET wins = wins + ?, losses = losses + ?, draws = draws + ?,
                        kills = kills + ?, deaths = deaths + ?
                    WHERE discord_id = ? AND is_active = 1
                ''', (wins, losses, draws, kills, deaths, discord_id))
                
                if cursor.rowcount == 0:
                    return False, "Player not found!"
                
                conn.commit()
                return True, "Statistics updated successfully!"
                
        except Exception as e:
            logger.error(f"Error updating stats: {e}")
            return False, f"Update failed: {str(e)}"
    
    def get_upcoming_matches(self, limit=10):
        """Get upcoming scheduled matches"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT m.*, p1.username as player1_name, p1.discord_id as player1_discord_id,
                           p2.username as player2_name, p2.discord_id as player2_discord_id
                    FROM matches m
                    JOIN players p1 ON m.player1_id = p1.id
                    JOIN players p2 ON m.player2_id = p2.id
                    WHERE m.status = 'scheduled' AND m.scheduled_time > CURRENT_TIMESTAMP
                    ORDER BY m.scheduled_time ASC
                    LIMIT ?
                ''', (limit,))
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting upcoming matches: {e}")
            return []
    
    def mark_reminder_sent(self, match_id: int):
        """Mark reminder as sent for a match"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE matches SET reminder_sent = 1 WHERE id = ?',
                    (match_id,)
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error marking reminder sent: {e}")
            return False
