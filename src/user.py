from __future__ import annotations

import sqlite3

from flask_login import UserMixin

from .utils import Password


class User(UserMixin):
    profile: Profile

    def __init__(
        self, conn: sqlite3.Connection, *, id: int, username: str, password: str
    ) -> None:
        self.conn = conn
        self.id = id
        self.username = username
        self.password = None

        self.profile = Profile.get(conn, id)

    @classmethod
    def get(cls, conn: sqlite3.Connection, id: int) -> User:
        cursor = conn.execute("SELECT * FROM USERS WHERE ID = ?", (id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            err = f"User {id} not found"
            raise ValueError(err)

        return cls(conn, **row) if row else None

    @classmethod
    def from_email(cls, conn: sqlite3.Connection, *, email: str, password: str) -> User:
        hashed_password = Password(password).hash_password

        cursor = conn.execute("SELECT * FROM USERS WHERE EMAIL = ?", (email,))
        row = cursor.fetchone()
        cursor.close()
        password = row["password"]

        if row is None:
            err = f"User {email} not found"
            raise ValueError(err)

        if password != hashed_password:
            err = f"Password does not match for user {email}"
            raise ValueError(err)

        return cls(conn, **row) if row else None


class Profile:
    def __init__(
        self,
        conn: sqlite3.Connection,
        *,
        user_id: int,
        picture: bytes | None = None,
        role: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        skills: str | None = None,
        experience: str | None = None,
        website: str | None = None,
        language: str | None = None,
        timezone: str | None = None,
    ):
        self.conn = conn
        self.user_id = user_id
        self.picture = picture
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.skills = skills
        self.experience = experience
        self.website = website
        self.language = language
        self.timezone = timezone

    @classmethod
    def get(cls, conn: sqlite3.Connection, user_id: int) -> Profile:
        cursor = conn.execute("SELECT * FROM PROFILES WHERE USER_ID = ?", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            err = f"Profile {user_id} not found"
            raise ValueError(err)

        return cls(conn, **row) if row else None
