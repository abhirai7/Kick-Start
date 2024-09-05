from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


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

    @property
    def user(self) -> User:
        from .user import User

        return User.get(self.conn, self.user_id)

    @staticmethod
    def all(conn: sqlite3.Connection, *, user_id: int | None = None) -> list[Gig]:
        if user_id is None:
            cursor = conn.execute("SELECT * FROM GIGS")
        else:
            cursor = conn.execute("SELECT * FROM GIGS WHERE USER_ID = ?", (user_id,))
        rows = cursor.fetchall()
        cursor.close()

        return [Gig(conn, **row) for row in rows]

    @property
    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "picture": self.picture,
            "created_at": self.created_at,
        }


# gig.json['title'] 