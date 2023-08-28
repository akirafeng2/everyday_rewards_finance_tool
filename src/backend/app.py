from flask import Flask, request, render_template, abort, session, redirect, url_for

from .backend import FileSystem
from .. import SETTINGS

app = Flask(__name__)

FS = FileSystem(SETTINGS.FINANCE_FILE_PATH, SETTINGS)

@app.route('/api/update_new_receipts', methods = ['GET'])
def update_new_receipts():
    
    # check for most recent receipt date

    # pass recent receipt date to scraper container to scrape

    # process receipts to pandas df
    FS.receipts_to_dataframe()

    # upload df to item df

    # move receipts to year/month folder

    # delete tmp folder
    pass