from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'secret-key'  # Required for session usage


#
# quiz_questions
#
quiz_questions = {
    "1": {
        "quiz_id": "1",
        "question": "Which Tire compound is shown in the image?",
        "image": "test.png",
        "options": [
            {"label": "Medium"},
            {"label": "Wet"},
            {"label": "Intermediate"},
            {"label": "Hard"}
        ],
        "correct": "Medium",
        "next_question": "2"
    },
    "2": {
        "quiz_id": "2",
        "question": "Your car is currently on Soft tires with very little wear and it's beginning to rain on the track. What is the right action?",
        "options": [
            {"label": "Switch to RED", "img": "test.png"},
            {"label": "Switch to BLUE", "img": "test.png"},
            {"label": "Switch to WHITE", "img": "test.png"},
            {"label": "Switch to GREEN", "img": "test.png"}
        ],
        "correct": "Switch to GREEN",
        "next_question": "3"
    },
    "3": {
        "quiz_id": "3",
        "question": "This is the current status of your tires. There are 18 laps left. What should you do?",
        "image": "test.png",
        "options": [
            {"label": "Box the lap and switch to a new set of tires."},
            {"label": "Go for a few more lap. Not all the tires have lots of wear."}
        ],
        "correct": "Box the lap and switch to a new set of tires.",
        "next_question": "end"
    }
}

#
# home route
#
@app.route('/')
def home():
    return render_template('home.html')


#
# Space for Natal routes
#


#
# quiz_start route
#
@app.route('/quiz_start', methods=['GET', 'POST'])
def quiz_start():
    if request.method == 'POST':
        session['answers'] = {}
        return redirect(url_for('quiz', quiz_id='1'))
    return render_template('quiz_start.html')

@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    if quiz_id not in quiz_questions:
        return "Quiz question not found", 404

    question = quiz_questions[quiz_id]

    if 'answers' not in session:
        session['answers'] = {}

    if request.method == 'POST':
        selected_answer = request.form.get('answer', '').strip()
        errors = {}

        if not selected_answer:
            errors['answer'] = "Please select an answer."
            return render_template('quiz.html', question=question, errors=errors)

        session['answers'][quiz_id] = selected_answer
        session.modified = True

        next_q = question.get('next_question', 'end')
        if next_q == 'end':
            return redirect(url_for('quiz_results'))

        return redirect(url_for('quiz', quiz_id=next_q))

    return render_template('quiz.html', question=question, errors={})
#
# quiz_results route
#
@app.route('/quiz_results')
def quiz_results():
    answers = session.get('answers', {})
    results = []
    score = 0

    for qid, qdata in quiz_questions.items():
        # Clean up both answers for a fair comparison
        user_answer = answers.get(qid, '').strip()
        correct_answer = qdata["correct"].strip()
        is_correct = user_answer.lower() == correct_answer.lower()  # case-insensitive

        if is_correct:
            score += 1

        results.append({
            "question": qdata["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    return render_template(
        'quiz_results.html',
        score=score,
        total=len(quiz_questions),
        results=results
    )


if __name__ == '__main__':
    app.run(debug=True)
