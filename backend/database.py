import sqlite3
import logging
from datetime import datetime
from typing import Optional, List, Tuple

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "bot_database.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # User XP table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_xp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 0,
                last_xp_time TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(guild_id, user_id)
            )
        ''')
        
        # Activity streaks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_streaks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                activity_name TEXT,
                streak_count INTEGER DEFAULT 0,
                last_activity_time TIMESTAMP,
                UNIQUE(guild_id, user_id)
            )
        ''')
        
        # Guild configuration table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guild_config (
                guild_id INTEGER PRIMARY KEY,
                enabled BOOLEAN DEFAULT 0,
                log_channel INTEGER,
                target_role INTEGER,
                auto_roles BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Custom XP roles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS custom_xp_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                level INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                UNIQUE(guild_id, level)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_xp_guild ON user_xp(guild_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_xp_user ON user_xp(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_xp_xp ON user_xp(xp DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_streaks_guild ON activity_streaks(guild_id)')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    # User XP Methods
    def get_user_xp(self, guild_id: int, user_id: int) -> dict:
        """Get user XP data."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT xp, level, last_xp_time FROM user_xp
            WHERE guild_id = ? AND user_id = ?
        ''', (guild_id, user_id))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "xp": result[0],
                "level": result[1],
                "last_xp_time": result[2]
            }
        return {"xp": 0, "level": 0, "last_xp_time": None}
    
    def add_xp(self, guild_id: int, user_id: int, xp_amount: int) -> Tuple[bool, int]:
        """Add XP to user and return (leveled_up, new_level)."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get current XP
        current_data = self.get_user_xp(guild_id, user_id)
        new_xp = current_data["xp"] + xp_amount
        new_level = new_xp // 100
        leveled_up = new_level > current_data["level"]
        
        # Update or insert
        cursor.execute('''
            INSERT INTO user_xp (guild_id, user_id, xp, level, last_xp_time)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(guild_id, user_id) DO UPDATE SET
                xp = ?,
                level = ?,
                last_xp_time = ?
        ''', (guild_id, user_id, new_xp, new_level, datetime.now(),
              new_xp, new_level, datetime.now()))
        
        conn.commit()
        conn.close()
        
        return leveled_up, new_level
    
    def get_leaderboard(self, guild_id: int, limit: int = 100) -> List[Tuple]:
        """Get leaderboard for a guild."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, xp, level FROM user_xp
            WHERE guild_id = ?
            ORDER BY xp DESC
            LIMIT ?
        ''', (guild_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_user_rank(self, guild_id: int, user_id: int) -> Optional[int]:
        """Get user's rank in guild."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) + 1 FROM user_xp
            WHERE guild_id = ? AND xp > (
                SELECT xp FROM user_xp WHERE guild_id = ? AND user_id = ?
            )
        ''', (guild_id, guild_id, user_id))
        
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def get_total_users(self, guild_id: int) -> int:
        """Get total users with XP in guild."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM user_xp WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
    
    # Streak Methods
    def get_streak(self, guild_id: int, user_id: int) -> dict:
        """Get user's activity streak."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT activity_name, streak_count, last_activity_time
            FROM activity_streaks
            WHERE guild_id = ? AND user_id = ?
        ''', (guild_id, user_id))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "activity": result[0],
                "count": result[1],
                "last_time": datetime.fromisoformat(result[2]) if result[2] else None
            }
        return {"activity": None, "count": 0, "last_time": None}
    
    def update_streak(self, guild_id: int, user_id: int, activity_name: str, streak_count: int):
        """Update user's activity streak."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activity_streaks (guild_id, user_id, activity_name, streak_count, last_activity_time)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(guild_id, user_id) DO UPDATE SET
                activity_name = ?,
                streak_count = ?,
                last_activity_time = ?
        ''', (guild_id, user_id, activity_name, streak_count, datetime.now(),
              activity_name, streak_count, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_top_streaks(self, guild_id: int, limit: int = 10) -> List[Tuple]:
        """Get top streaks in guild."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, activity_name, streak_count FROM activity_streaks
            WHERE guild_id = ? AND streak_count > 0
            ORDER BY streak_count DESC
            LIMIT ?
        ''', (guild_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    # Guild Config Methods
    def get_guild_config(self, guild_id: int) -> dict:
        """Get guild configuration."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT enabled, log_channel, target_role, auto_roles
            FROM guild_config WHERE guild_id = ?
        ''', (guild_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "enabled": bool(result[0]),
                "log_channel": result[1],
                "target_role": result[2],
                "auto_roles": bool(result[3])
            }
        return {
            "enabled": False,
            "log_channel": None,
            "target_role": None,
            "auto_roles": False
        }
    
    def update_guild_config(self, guild_id: int, **kwargs):
        """Update guild configuration."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build update query dynamically
        fields = []
        update_values = []
        for key, value in kwargs.items():
            if key in ["enabled", "log_channel", "target_role", "auto_roles"]:
                fields.append(f"{key} = ?")
                update_values.append(value)
        
        if not fields:
            conn.close()
            return
        
        # Prepare values: [guild_id] + insert values + update values
        insert_values = [guild_id] + list(kwargs.values())
        all_values = insert_values + update_values
        
        cursor.execute(f'''
            INSERT INTO guild_config (guild_id, {", ".join(kwargs.keys())})
            VALUES (?, {", ".join(["?" for _ in kwargs])})
            ON CONFLICT(guild_id) DO UPDATE SET {", ".join(fields)}
        ''', all_values)
        
        conn.commit()
        conn.close()
    
    # Custom Roles Methods
    def add_custom_role(self, guild_id: int, level: int, role_id: int):
        """Add custom XP role."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO custom_xp_roles (guild_id, level, role_id)
            VALUES (?, ?, ?)
            ON CONFLICT(guild_id, level) DO UPDATE SET role_id = ?
        ''', (guild_id, level, role_id, role_id))
        
        conn.commit()
        conn.close()
    
    def get_custom_roles(self, guild_id: int) -> dict:
        """Get all custom roles for guild."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT level, role_id FROM custom_xp_roles
            WHERE guild_id = ?
        ''', (guild_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return {str(level): role_id for level, role_id in results}
    
    def remove_custom_role(self, guild_id: int, level: int):
        """Remove custom XP role."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM custom_xp_roles
            WHERE guild_id = ? AND level = ?
        ''', (guild_id, level))
        
        conn.commit()
        conn.close()
    
    # Utility Methods
    def backup_to_json(self, filename: str = "database_backup.json"):
        """Backup database to JSON file."""
        import json
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        backup_data = {
            "user_xp": [],
            "streaks": [],
            "guild_configs": [],
            "custom_roles": []
        }
        
        # Backup user XP
        cursor.execute('SELECT * FROM user_xp')
        for row in cursor.fetchall():
            backup_data["user_xp"].append({
                "guild_id": row[1],
                "user_id": row[2],
                "xp": row[3],
                "level": row[4]
            })
        
        # Backup streaks
        cursor.execute('SELECT * FROM activity_streaks')
        for row in cursor.fetchall():
            backup_data["streaks"].append({
                "guild_id": row[1],
                "user_id": row[2],
                "activity": row[3],
                "count": row[4]
            })
        
        conn.close()
        
        with open(filename, 'w') as f:
            json.dump(backup_data, f, indent=4)
        
        logger.info(f"Database backed up to {filename}")
        return filename

# Global database instance
db = Database()
