from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz, Survey, Question
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
bootstrap = Bootstrap(app)

responses = []
question_id = len(responses)

debug = DebugToolbarExtension(app)

@app.route("/")
def homepage():
    '''homepage with survey name, questions and start btn'''
    instructions = satisfaction_survey.instructions
    title = satisfaction_survey.title
    return render_template("homepage.html", instructions=instructions, title=title)

@app.route("/questions/<int:question_id>", methods=["GET", "POST"])
def questions(question_id):
    '''renders the first survey question'''
    question = satisfaction_survey.questions[question_id]

    return render_template("questions.html", question_id=question_id, question=question)