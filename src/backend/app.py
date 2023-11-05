from flask import Flask
import SETTINGS
from user.views import user_blueprint
from receipt.views import receipt_blueprint
from weighting.views import weighting_blueprint
from household.views import household_blueprint
from expenses.views import expenses_blueprint
from dashboard.views import dashboard_blueprint
from reset.views import reset_blueprint


# env = SETTINGS.ENV
# DB_CONN = DatabaseConnection2(SETTINGS.CONNECTION_DETAILS, env, "1") # get rid or profile_id here. save it in session
# within views and pass it through methods of DB_CONN within views
# FS = FileSystem(SETTINGS.FINANCE_FILE_PATH / env)

app = Flask(__name__)

app.secret_key = SETTINGS.SECRET_KEY
app.register_blueprint(user_blueprint, url_prefix="/api/user")
app.register_blueprint(receipt_blueprint, url_prefix="/api/receipt")
app.register_blueprint(weighting_blueprint, url_prefix="/api/weighting")
app.register_blueprint(household_blueprint, url_prefix="/api/household")
app.register_blueprint(expenses_blueprint, url_prefix="/api/expenses")
app.register_blueprint(dashboard_blueprint, url_prefix="/api/dashboard")
app.register_blueprint(reset_blueprint, url_prefix="/api/reset")
