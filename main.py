from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from backend.models import db
from backend.worker import celery
from backend.task import *
from datetime import timedelta
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "database/SponserConnect.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

# Redis Cache (use Render Redis URL)
app.config["CACHE_TYPE"] = "redis"
app.config["CACHE_REDIS_URL"] = os.environ.get("REDIS_URL")
app.config["CACHE_DEFAULT_TIMEOUT"] = 600

jwt = JWTManager(app)
db.init_app(app)

from backend.api import *

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    db.create_all()
    app.run()
