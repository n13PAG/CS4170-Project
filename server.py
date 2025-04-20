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
        "image": "question_1.png",
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
            {"label": "Switch to Red:", "img": "question_2_red.png"},
            {"label": "Switch to Blue:", "img": "question_2_blue.png"},
            {"label": "Switch to White:", "img": "question_2_white.png"},
            {"label": "Switch to Green:", "img": "question_2_green.png"}
        ],
        "correct": "Switch to Green:",
        "next_question": "3"
    },
    "3": {
        "quiz_id": "3",
        "question": "This is the current status of your tires. There are 18 laps left. What should you do?",
        "image": "question_3.png",
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

#
# quiz route
#

@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    if quiz_id == "end":
        return redirect(url_for('quiz_results'))

    if quiz_id not in quiz_questions:
        return "Quiz question not found", 404

    question = quiz_questions[quiz_id]
    selected_answer = None
    is_correct = None
    errors = {}

    # Track question number (as int) and total questions
    question_number = int(quiz_id)
    total_questions = len(quiz_questions)

    if 'answers' not in session:
        session['answers'] = {}

    if request.method == 'POST':
        selected_answer = request.form.get('answer', '').strip()

        if not selected_answer:
            errors['answer'] = "Please select an answer."
        else:
            session['answers'][quiz_id] = selected_answer
            session.modified = True

            is_correct = selected_answer.lower() == question['correct'].strip().lower()

            return render_template(
                'quiz.html',
                question=question,
                selected=selected_answer,
                is_correct=is_correct,
                errors=errors,
                show_feedback=True,
                next_question=question.get('next_question', 'end'),
                question_number=question_number,
                total_questions=total_questions
            )

    return render_template(
        'quiz.html',
        question=question,
        selected=None,
        is_correct=None,
        errors=errors,
        show_feedback=False,
        next_question=question.get('next_question', 'end'),
        question_number=question_number,
        total_questions=total_questions
    )



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
