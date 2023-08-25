from flask import Flask, request, render_template, abort, session, redirect, url_for

from scraper import EverydayRewardsScraper

import datetime

app = Flask(__name__)

app.secret_key = "my_secret_key"

@app.route('/api/scrape_everyday_rewards/entry', methods = ['GET','POST'])
def scrape_everyday_rewards_entry():
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        session['email'] = request.form.get('email')
        session['password'] = request.form.get('password')
        
        return redirect(url_for('scrape_everyday_rewards_pre_mfa'))
    
    return render_template('email_form.html')    


@app.route('/api/scrape_everyday_rewards/start', methods=['GET'])
def scrape_everyday_rewards_pre_mfa():

    name = session.pop('name')
    email = session.pop('email')
    password = session.pop('password')

    global scraper 
    
    scraper = EverydayRewardsScraper()

    scraper.set_downloads(name)

    scraper.start()

    scraper.switch_to_iframe()

    scraper.input_login_details(email, password)
  
    return render_template('sms_form.html')
    # data = request.json

    # if data:
    #     expected_keys = ['name', 'email', 'password']

    #     if all(key in data for key in expected_keys):
            
    #         global scraper 
            
    #         scraper = EverydayRewardsScraper()

    #         name = data.get('name')
    #         scraper.set_downloads(name)

    #         scraper.start()

    #         scraper.switch_to_iframe()

    #         email = data.get('email')
    #         password = data.get('password')

    #         scraper.input_login_details(email, password)
    #     else:
    #         abort(404, description = "Missing Inputs") 
    # else:
    #     abort(404, description = "Missing Inputs") 
    # return render_template('sms_form.html')


@app.route('/api/scrape_everyday_rewards/continue', methods = ['POST'])
def scrape_everyday_rewards_post_mfa():
        
    sms_code = request.form.get('SMS Code')

    date_string = "01Jan2000"
    date_format = "%d%b%Y"
    recent_date = datetime.strptime(date_string, date_format)
    
    
    global scraper

    scraper.input_mfa_code(sms_code)

    scraper.navigate_to_receipt_page()

    scraper.download_receipts(recent_date, 50)
    scraper.stop()

    return "Receipts downloaded successfully"