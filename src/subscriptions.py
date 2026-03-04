from src.loader import load_to_sqlite
from sqlalchemy import create_engine, text
from os import getenv
from dotenv import load_dotenv

class SubscriptionManager:
    def __init__(self):
        load_dotenv()
        self._engine = create_engine(getenv("DATABASE_URL"))
        self._conn = self._engine.connect()
    
    def close(self):
        self._conn.close()
        self._engine.dispose()

    def subscribe_user_to_source(self, user_id, source_id):
        # Check if source and user exists
        row = self._conn.execute(
            text(
                "SELECT * FROM sources WHERE id = :source_id"
            ),{"source_id": source_id}
        ).fetchone()
        if row is None:
            raise ValueError("Not such a source")
        row = self._conn.execute(
            text(
                "SELECT * FROM users WHERE id = :user_id"
            ),{"user_id": user_id}
        ).fetchone()
        if row is None:
            raise ValueError("Not such a user")
        
        #Adding subscription
        self._conn.execute(
            text(
                "INSERT INTO user_subscriptions(user_id, source_id) VALUES (:user_id, :source_id)"
            ),{"user_id": user_id, "source_id": source_id}
        )
        self._conn.commit()

    def get_user_feed(self, user_id):
        """Return user feed as dictionary where name of source are keys and values are links"""
        # Checking if user exists
        row = self._conn.execute(
            text(
                "SELECT * FROM users WHERE id = :user_id"
            ),{"user_id": user_id}
        ).fetchone()
        if row is None:
            raise ValueError("Not such a user")
        
        # Retrieving feed
        rows = self._conn.execute(
            text(
                """
                SELECT s.source, s.link
                FROM sources as s
                INNER JOIN user_subscriptions as us ON s.id = us.source_id
                WHERE us.user_id = :user_id
                """
            ),{"user_id": user_id}
        ).fetchall()

        data = {}
        for row in rows:
            data[row.source] = row.link
        
        return data
    
    def delete_subscription(self, user_id, source_id):
        result = self._conn.execute(
            text("DELETE FROM user_subscriptions WHERE user_id = :user_id AND source_id = :source_id"),
            {"user_id": user_id, "source_id": source_id}
        )

        if result.rowcount == 0:
            print("No such a subscription")
            return
        
        self._conn.commit()