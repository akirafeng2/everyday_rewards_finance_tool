from flask import Flask, request, render_template, abort, session, redirect, url_for

from backend import FileSystem, DatabaseConnection2, Calculations
from routes.register_routes import api
import SETTINGS

env = SETTINGS.ENV
DB_CONN = DatabaseConnection2(SETTINGS.CONNECTION_DETAILS, env, "1") # get rid or profile_id here. save it in session within views and pass it through methods of DB_CONN within views
FS = FileSystem(SETTINGS.FINANCE_FILE_PATH / env)

app = Flask(__name__)
app.secret_key = SETTINGS.SECRET_KEY
app.DB_CONN = DB_CONN
app.register_blueprint(api, url_prefix="/api")
