from flask import Flask, render_template
from datetime import datetime
import re

app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello, Flask!"

@app.route('/')
def home():
    return render_template('home.html')