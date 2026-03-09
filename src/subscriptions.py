from sqlalchemy import create_engine, text
from os import getenv
from dotenv import load_dotenv

class SubscriptionManager:
    def __init__(self, db_url = None):
        load_dotenv()
        self._engine = create_engine(db_url or getenv("DATABASE_URL"))
        self.conn = self._engine.connect()
    
    def close(self):
        self.conn.close()
        self._engine.dispose()

    def subscribe_user_to_source(self, user_id, source_id):
        # Check if source and user exists
        row = self.conn.execute(
            text(
                "SELECT * FROM sources WHERE id = :source_id"
            ),{"source_id": source_id}
        ).fetchone()
        if row is None:
            raise ValueError("No such a source")
        row = self.conn.execute(
            text(
                "SELECT * FROM users WHERE id = :user_id"
            ),{"user_id": user_id}
        ).fetchone()
        if row is None:
            raise ValueError("No such a user")
        
        #Adding subscription
        self.conn.execute(
            text(
                "INSERT INTO user_subscriptions(user_id, source_id) VALUES (:user_id, :source_id)"
            ),{"user_id": user_id, "source_id": source_id}
        )
        self.conn.commit()

    def get_user_feed(self, user_id):
        """Return user feed as dictionary where name of source are keys and values are links"""
        # Checking if user exists
        row = self.conn.execute(
            text(
                "SELECT * FROM users WHERE id = :user_id"
            ),{"user_id": user_id}
        ).fetchone()
        if row is None:
            raise ValueError("No such a user")
        
        # Retrieving feed
        rows = self.conn.execute(
            text(
                """
                SELECT s.id, s.source, s.link
                FROM sources as s
                INNER JOIN user_subscriptions as us ON s.id = us.source_id
                WHERE us.user_id = :user_id
                """
            ),{"user_id": user_id}
        ).fetchall()

        return {row.source: (row.id, row.link) for row in rows}
    
    def unsubscripe(self, user_id, source_id):
        result = self.conn.execute(
            text("DELETE FROM user_subscriptions WHERE user_id = :user_id AND source_id = :source_id"),
            {"user_id": user_id, "source_id": source_id}
        )

        if result.rowcount == 0:
            raise ValueError("No such a subscription")
        
        self.conn.commit()

    def close(self):
        self.conn.close()
        self._engine.dispose()