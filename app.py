from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz, Survey, Question
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
bootstrap = Bootstrap(app)
debug = DebugToolbarExtension(app)

# allows new instances of survey results
SESSION_KEY = "responses"

@app.route("/")
def homepage():
    '''homepage with survey name, questions and start btn'''
    session[SESSION_KEY] = []
    instructions = satisfaction_survey.instructions
    title = satisfaction_survey.title
    return render_template("homepage.html", instructions=instructions, title=title)

@app.route("/questions/<int:question_id>", methods=["GET", "POST"])
def questions(question_id):
    '''renders the first survey question. prevents user from skipping or resubmitting questions'''
    responses = session[SESSION_KEY]

    if request.method in ["GET", "POST"]:
        # check for invalid response
        if question_id > len(responses):
            flash(f"Invalid question id: {question_id}")
            return redirect(f"/questions/{len(responses)}")
        elif len(responses) == len(satisfaction_survey.questions):
            return redirect("/survey_end")
        else:
            question = satisfaction_survey.questions[question_id].question
            choices = satisfaction_survey.questions[question_id].choices
            return render_template("questions.html", question=question, choices=choices)
    else:
        # redirect to questions/len(responses
        return redirect(f"/questions/{len(responses)}")

@app.route("/responses", methods=["POST"])
def collect_responses():
    '''get answer and add to responses, redirects to the next question or survey_end page'''
    responses = session[SESSION_KEY]

    if request.method == "POST":
        answer = request.form.get("option", None)
        # check for invalid response
        if not answer:
            return redirect(f"/questions/{len(responses)}")

        responses.append(answer)
        session[SESSION_KEY] = responses
        survey_length = len(satisfaction_survey.questions)

        if survey_length != len(responses):
            return redirect(f"/questions/{len(responses)}")
        else:
            return redirect("/survey_end")
    else:
        # redirect to questions/len(responses)
        return redirect(f"/questions/{len(responses)}")

@app.route("/survey_end")
def survey_end():
    '''notify user that survey has been completed'''
    return render_template("survey_end.html")

@app.route("/summary")
def summary():
    '''temp route - placeholder for user summaries'''
    return render_template("summary.html")