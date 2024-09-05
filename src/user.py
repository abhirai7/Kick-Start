from __future__ import annotations

import contextlib
import sqlite3
from typing import TYPE_CHECKING

from flask_login import UserMixin

from .utils import Password

if TYPE_CHECKING:
    from .gig import Gig


class User(UserMixin):
    profile: Profile

    def __init__(
        self, conn: sqlite3.Connection, *, id: int, email: str, password: str, **kwargs
    ) -> None:
        self.conn = conn
        self.id = id
        self.email = email
        self.password = None

        with contextlib.suppress(ValueError):
            self.profile = Profile.get(conn, id)
        self.created_at = kwargs.pop("created_at", None)

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
        hashed_password = Password(password).hex

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

    @classmethod
    def exists(cls, conn: sqlite3.Connection, *, email: str) -> bool:
        cursor = conn.execute("SELECT * FROM USERS WHERE EMAIL = ?", (email,))
        row = cursor.fetchone()
        cursor.close()
        return row is not None

    @classmethod
    def create(cls, conn: sqlite3.Connection, *, email: str, password: str) -> User:
        hashed_password = Password(password).hex

        cursor = conn.execute(
            "INSERT INTO USERS (EMAIL, PASSWORD) VALUES (?, ?)",
            (email, hashed_password),
        )
        conn.commit()
        cursor.close()

        user_id = cursor.lastrowid
        return cls(conn, id=user_id, email=email, password=hashed_password)

    def add_gig_review(self, gig: Gig, *, rating: int, review: str) -> None:
        cursor = self.conn.execute(
            "INSERT INTO GIG_REVIEWS (GIG_ID, USER_ID, RATING, REVIEW) VALUES (?, ?, ?, ?)",
            (gig.id, self.id, rating, review),
        )
        self.conn.commit()
        cursor.close()

    def add_gig(
        self, *, title: str, description: str, price: float, picture: bytes
    ) -> Gig:
        from .gig import Gig

        cursor = self.conn.execute(
            "INSERT INTO GIGS (USER_ID, TITLE, DESCRIPTION, PRICE, PICTURE) VALUES (?, ?, ?, ?, ?)",
            (self.id, title, description, price, picture),
        )
        self.conn.commit()
        cursor.close()

        gig_id = cursor.lastrowid
        return Gig(
            self.conn,
            id=gig_id,
            user_id=self.id,
            title=title,
            description=description,
            price=price,
            picture=picture,
            created_at=None,
        )

    def get_gig(self, gig_id: int) -> Gig:
        from .gig import Gig

        cursor = self.conn.execute("SELECT * FROM GIGS WHERE ID = ?", (gig_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            err = f"Gig {gig_id} not found"
            raise ValueError(err)

        return Gig(self.conn, **row) if row else None

    def delete_gig(self, gig_id: int) -> None:
        cursor = self.conn.execute(
            "DELETE FROM GIGS WHERE ID = ? AND USER_ID = ?", (gig_id, self.id)
        )
        self.conn.commit()
        cursor.close()

    def get_gigs(self, user_id: int) -> list[Gig]:
        return Gig.all(self.conn, user_id=user_id)

    @property
    def json(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at,
            "profile": self.profile.json,
            "gigs": [gig.json for gig in self.get_gigs(self.id)],
        }

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

    VALID_X = (
        "user_id",
        "picture",
        "role",
        "first_name",
        "last_name",
        "email",
        "phone",
        "address",
        "skills",
        "experience",
        "website",
        "language",
        "timezone",
    )

    def set_x(self, x: str, value: str) -> None:
        cursor = self.conn.execute(
            f"UPDATE PROFILES SET {x.upper()} = ? WHERE USER_ID = ?",
            (value, self.user_id),
        )
        self.conn.commit()
        cursor.close()

    def __getattr__(self, name: str) -> str | None:
        if name in self.VALID_X:
            return getattr(self, name)
        error = f"{self.__class__.__name__} has no attribute {name}"
        raise AttributeError(error)

    if TYPE_CHECKING:

        def set_user_id(self, user_id: int) -> None:
            ...

        def set_picture(self, picture: bytes) -> None:
            ...

        def set_role(self, role: str) -> None:
            ...

        def set_first_name(self, first_name: str) -> None:
            ...

        def set_last_name(self, last_name: str) -> None:
            ...

        def set_email(self, email: str) -> None:
            ...

        def set_phone(self, phone: str) -> None:
            ...

        def set_skills(self, skills: str) -> None:
            ...

        def set_experience(self, experience: str) -> None:
            ...

        def set_website(self, website: str) -> None:
            ...

        def set_language(self, language: str) -> None:
            ...

        def set_timezone(self, timezone: str) -> None:
            ...

    @property
    def json(self):
        return {
            "user_id": self.user_id,
            "picture": self.picture,
            "role": self.role,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "skills": self.skills,
            "experience": self.experience,
            "website": self.website,
            "language": self.language,
            "timezone": self.timezone,
        }