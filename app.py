from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

responses = []

@app.route("/")
def homepage():
    '''homepage with survey name, questions and start btn'''
    # text = satisfaction_survey.text
    return render_template("homepage.html")