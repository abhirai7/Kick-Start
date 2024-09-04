from __future__ import annotations

import os
import pathlib
import sqlite3

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from src.utils import sqlite_row_factory

app = Flask(__name__)

login_manager = LoginManager(app)

sql = pathlib.Path("sql.sql").read_text()
conn = sqlite3.connect("database.db", check_same_thread=False)
conn.executescript(sql)

conn.row_factory = sqlite_row_factory

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app.secret_key = f"{SECRET_KEY}"
csrf = CSRFProtect(app)
login_manager.init_app(app)

from .login_manager import *  # noqa
from .routes import *  # noqa
