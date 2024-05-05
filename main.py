from flask import Flask, render_template, redirect, request, send_from_directory, session
from werkzeug.utils import secure_filename

import sqlite3
import os
import datetime

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = 'fggsagejhtewr'

# socket = SocketIO(app)
# somelist = ['mela', 'pera', 'banana', 'arancia']
i=0
DataBasePath = './database.db'
StaticsPath = "./static"


@app.route('/')
def index():
    session['refresh_time'] = 10
    return render_template('gallery.html')

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

