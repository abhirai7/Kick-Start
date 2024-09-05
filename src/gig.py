from __future__ import annotations

import sqlite3


class Gig:
    def __init__(
        self,
        conn: sqlite3.Connection,
        *,
        id: int,
        user_id: int,
        title: str,
        description: str,
        price: float,
        picture: bytes | None = None,
        created_at: str,
    ):
        self.conn = conn
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.price = price
        self.picture = picture
        self.created_at = created_at
