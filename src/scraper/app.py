from flask import Flask, request, render_template, abort, session, redirect, url_for, jsonify
from flask_cors import CORS

from markupsafe import escape

from scraper import EverydayRewardsScraper

from datetime import datetime

import SETTINGS

app = Flask(__name__)

app.secret_key = SETTINGS.SECRET_KEY

CORS(
    app,
    origins=[f"http://{SETTINGS.IP_ADDRESS}:5173", "http://127.0.0.1:5173", "http://localhost:5173"],
    supports_credentials=True,
)


def wants_json() -> bool:
    """True for the React app's XHR requests, False for the legacy HTML form flow"""
    return request.accept_mimetypes.best_match(['application/json', 'text/html']) == 'application/json'


def start_scraper(household: str, name: str, email: str, password: str) -> None:
    global scraper

    scraper = EverydayRewardsScraper()
    scraper.set_downloads(household, name)
    scraper.start()
    scraper.switch_to_iframe()
    scraper.input_login_details(email, password)


@app.route('/api/scrape_everyday_rewards/<household>/<name>/<date_to>/entry', methods = ['GET','POST'])
def scrape_everyday_rewards_entry(household ,name, date_to):
    if request.method == 'POST':
        session['household'] = escape(household)
        session['name'] = escape(name)
        session['email'] = request.form.get('email')
        session['password'] = request.form.get('password')
        session['date_to'] = escape(date_to)

        if wants_json():
            try:
                start_scraper(
                    session.pop('household'), session.pop('name'), session.pop('email'), session.pop('password')
                )
            except Exception as e:
                print(e)
                return jsonify({'error': 'login'}), 401
            return jsonify({'status': 'mfa_required'}), 200

        return redirect(url_for('scrape_everyday_rewards_pre_mfa'))

    return render_template('email_form.html')    


@app.route('/api/scrape_everyday_rewards/start', methods=['GET'])
def scrape_everyday_rewards_pre_mfa():
    start_scraper(session.pop('household'), session.pop('name'), session.pop('email'), session.pop('password'))
    return render_template('sms_form.html')


@app.route('/api/scrape_everyday_rewards/continue', methods = ['POST'])
def scrape_everyday_rewards_post_mfa():
        
    sms_code = request.form.get('SMS Code')

    date_string = session.pop('date_to')

    date_format = "%d%b%Y"
    recent_date = datetime.strptime(date_string, date_format)
    
    
    global scraper

    try:
        scraper.input_mfa_code(sms_code)
        scraper.navigate_to_receipt_page()
    except Exception as e:
        print(e)
        session['date_to'] = date_string
        if wants_json():
            return jsonify({'error': 'mfa'}), 401
        raise

    scraper.download_receipts(recent_date, 50)
    scraper.stop()

    if wants_json():
        return jsonify({'status': 'downloaded'}), 200

    return redirect(f"http://{SETTINGS.IP_ADDRESS}:5050/api/receipt/insert_receipts_to_db")
