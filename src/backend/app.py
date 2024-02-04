from flask import Flask, abort
from . import SETTINGS, user, receipt, weighting, household, expenses, reset
from flask_cors import CORS

from supertokens_python.framework.flask import Middleware

from supertokens_python import init, InputAppInfo, SupertokensConfig, get_all_cors_headers
from supertokens_python.recipe import emailpassword, session, dashboard

init(
    app_info=InputAppInfo(
        app_name="erapp",
        api_domain="http://127.0.0.1:5050",
        website_domain="http://127.0.0.1:5173",
        api_base_path="/api/auth",
        website_base_path="/login"
    ),
    supertokens_config=SupertokensConfig(
        connection_uri="http://supertokens:3567",
        # api_key=<API_KEY(if configured)>
    ),
    framework='flask',
    recipe_list=[
        session.init(),  # initializes session features
        emailpassword.init(),
        dashboard.init()
    ]
)

# env = SETTINGS.ENV
# DB_CONN = DatabaseConnection2(SETTINGS.CONNECTION_DETAILS, env, "1") # get rid or profile_id here. save it in session
# within views and pass it through methods of DB_CONN within views
# FS = FileSystem(SETTINGS.FINANCE_FILE_PATH / env)

app = Flask(__name__)
Middleware(app)
CORS(
    app=app,
    # origins=[
    #     "http://172.18.0.1:5173"
    # ],
    supports_credentials=True,
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

app.secret_key = SETTINGS.SECRET_KEY
app.register_blueprint(user.views.blueprint, url_prefix="/api/user")
app.register_blueprint(receipt.views.blueprint, url_prefix="/api/receipt")
app.register_blueprint(weighting.views.blueprint, url_prefix="/api/weighting")
app.register_blueprint(household.views.blueprint, url_prefix="/api/household")
app.register_blueprint(expenses.views.blueprint, url_prefix="/api/expenses")
# app.register_blueprint(dashboard.views.blueprint, url_prefix="/api/dashboard")
app.register_blueprint(reset.views.blueprint, url_prefix="/api/reset")
# This is required since if this is not there, then OPTIONS requests for
# the APIs exposed by the supertokens' Middleware will return a 404


@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def catch_all(u_path: str):
    abort(404)
