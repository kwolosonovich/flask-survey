from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz, Survey, Question

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

responses = []

@app.route("/")
def homepage():
    '''homepage with survey name, questions and start btn'''
    instructions = satisfaction_survey.instructions
    title = satisfaction_survey.title
    return render_template("homepage.html", instructions=instructions, title=title)