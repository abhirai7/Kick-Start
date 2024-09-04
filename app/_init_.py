from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_security import Security

app = Flask(__name__,template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///freelance-platform.db"
app.config["SECRET_KEY"] = "secret_key_here"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
security = Security(app)

from app import routes