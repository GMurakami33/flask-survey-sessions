from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "surveys"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def start():
    """Starting page that provides title, instructions, and start button"""
    return render_template('home.html', survey=survey)

@app.route('/start_survey', methods=['POST'])
def start_survey():
    """Initialize session and start the survey"""
    session['responses'] = []  # Initialize the responses session as an empty list
    return redirect('/questions/0')  

@app.route('/questions/<int:question_index>', methods=['GET', 'POST'])
def show_questions(question_index):
    """Start providing questions"""
    if question_index >= len(survey.questions):
        flash('You are trying to access an invalid question.')
        return redirect('/thank_you')
    
    question = survey.questions[question_index]
    return render_template('questions.html', question=question)

@app.route('/answer', methods=['POST'])
def save_answers():
    selection = request.form.get('answer')
    responses = session.get('responses', [])
    responses.append(selection)
    session['responses'] = responses

    question_index = len(responses)
    if question_index < len(survey.questions):
        return redirect(f'/questions/{question_index}')
    else:
        return redirect('/thank_you')

@app.route('/thank_you')
def say_thanks():
    session.pop('responses', None)
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run()