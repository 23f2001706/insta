"""Conversation storage and retrieval"""
import json
import sqlite3
import logging
from datetime import datetime
from .config import Config

logger = logging.getLogger(__name__)


class ConversationStore:
    """Manage conversation history in SQLite database"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DB_PATH
        self._initialize_db()
    
    def _initialize_db(self):
        """Create database tables if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    username TEXT,
                    messages TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def add_message(self, user_id: str, role: str, content: str, username: str = None):
        """Add a message to conversation history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            }
            
            cursor.execute("SELECT messages FROM conversations WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            
            if result:
                messages = json.loads(result[0])
                messages.append(message)
                cursor.execute(
                    "UPDATE conversations SET messages = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
                    (json.dumps(messages), user_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO conversations (user_id, username, messages) VALUES (?, ?, ?)",
                    (user_id, username, json.dumps([message]))
                )
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error adding message: {e}")
    
    def get_history(self, user_id: str) -> list:
        """Get conversation history for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT messages FROM conversations WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return json.loads(result[0])
            return []
        except Exception as e:
            logger.error(f"Error getting history: {e}")
            return []
    
    def clear_history(self, user_id: str):
        """Clear conversation history for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
            logger.info(f"Cleared history for user {user_id}")
        except Exception as e:
            logger.error(f"Error clearing history: {e}")
