from flask import Flask, request, render_template, abort

from scraper import EverydayRewardsScraper

app = Flask(__name__)


@app.route('/api/scrape_everyday_rewards/start', methods=['POST'])
def scrape_everyday_rewards_pre_mfa():

    data = request.json

    if data:
        expected_keys = ['name', 'email', 'password']

        if all(key in data for key in expected_keys):
            
            global scraper 
            
            scraper = EverydayRewardsScraper()

            name = data.get('name')
            scraper.set_downloards(name)

            scraper.start()

            scraper.switch_to_iframe()

            email = data.get('email')
            password = data.get('password')

            scraper.input_login_details(email, password)
        else:
            abort(404, description = "Missing Inputs") 
    else:
        abort(404, description = "Missing Inputs") 
    return render_template('form.html')


@app.route('/api/scrape_everyday_rewards/continue', methods = ['POST'])
def scrape_everyday_rewards_post_mfa():
        
    sms_code = request.form.get('SMS Code')
    
    global scraper

    scraper.input_mfa_code(sms_code)

    scraper.navigate_to_receipt_page()

    scraper.download_receipts("01Jan2000", 50)
    scraper.stop()

    return "Receipts downloaded successfully"
