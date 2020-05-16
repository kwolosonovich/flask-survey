from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz, Survey, Question
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
bootstrap = Bootstrap(app)
debug = DebugToolbarExtension(app)


responses = []

@app.route("/")
def homepage():
    '''homepage with survey name, questions and start btn'''
    instructions = satisfaction_survey.instructions
    title = satisfaction_survey.title
    return render_template("homepage.html", instructions=instructions, title=title)

@app.route("/questions/<int:question_id>", methods=["GET", "POST"])
def questions(question_id):
    '''renders the first survey question'''

    if question_id > len(responses):
        return redirect(f"/questions/{len(responses)}")
    else:
        question = satisfaction_survey.questions[question_id].question
        choices = satisfaction_survey.questions[question_id].choices

        return render_template("questions.html", question=question, choices=choices)

@app.route("/responses", methods=["POST"])
def collect_responses():
    answer = request.form["option"]
    responses.append(answer)
    survey_length = len(satisfaction_survey.questions)
    if survey_length != len(responses):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect("/survey_end")

@app.route("/survey_end")
def survey_end():
    '''notify user that survey has been completed'''
    return render_template("survey_end.html")