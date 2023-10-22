from flask import Flask, request, render_template, abort, session, redirect, url_for
from . import SETTINGS, user, receipt


# env = SETTINGS.ENV
# DB_CONN = DatabaseConnection2(SETTINGS.CONNECTION_DETAILS, env, "1") # get rid or profile_id here. save it in session within views and pass it through methods of DB_CONN within views
# FS = FileSystem(SETTINGS.FINANCE_FILE_PATH / env)

app = Flask(__name__)

app.secret_key = SETTINGS.SECRET_KEY
app.register_blueprint(user.views.blueprint, url_prefix="/api/user")
app.register_blueprint(receipt.views.blueprint, url_prefix="/api/receipt")