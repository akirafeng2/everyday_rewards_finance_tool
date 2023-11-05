from flask import Flask
from . import SETTINGS, user, receipt, weighting, household, expenses, dashboard, reset


# env = SETTINGS.ENV
# DB_CONN = DatabaseConnection2(SETTINGS.CONNECTION_DETAILS, env, "1") # get rid or profile_id here. save it in session
# within views and pass it through methods of DB_CONN within views
# FS = FileSystem(SETTINGS.FINANCE_FILE_PATH / env)

app = Flask(__name__)

app.secret_key = SETTINGS.SECRET_KEY
app.register_blueprint(user.views.blueprint, url_prefix="/api/user")
app.register_blueprint(receipt.views.blueprint, url_prefix="/api/receipt")
app.register_blueprint(weighting.views.blueprint, url_prefix="/api/weighting")
app.register_blueprint(household.views.blueprint, url_prefix="/api/household")
app.register_blueprint(expenses.views.blueprint, url_prefix="/api/expenses")
app.register_blueprint(dashboard.views.blueprint, url_prefix="/api/dashboard")
app.register_blueprint(reset.views.blueprint, url_prefix="/api/reset")
