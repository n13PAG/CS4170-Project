import datetime
import time
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
        "image": "YELLOW_tire.png",
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
            {"label": "Switch to Red:", "img": "RED_tire.png"},
            {"label": "Switch to Blue:", "img": "BLUE_tire.png"},
            {"label": "Switch to White:", "img": "WHITE_tire.png"},
            {"label": "Switch to Green:", "img": "GREEN_tire.png"}
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
# Tire Info
#
tire_info = {
    "0": {
        "id": "0",
        "type": "Wet",
        "name": "Wet",
        "color": "blue",
        "description": "The full wet tyres are the most effective for heavy rain, capable of dispersing impressive quantities of water. But if it rains heavily, visibility rather than grip causes issues, leading to race stoppages on occasions. The profile (deeper grooves) delivers increased resistance to aquaplaning, which gives the tyre more grip in heavy rain.",
        "image": "BLUE_tire.png"
    },
    "1": {
        "id": "1",
        "type": "Intermediate",
        "name": "Intermediate",
        "color": "green",
        "description": "The intermediates are the most versatile of the rain tyres. They can be used on a wet track with no standing water, as well as a drying surface. The compound has been designed to have a wide working range, guaranteeing a wide crossover window both with the slicks and the full wets.",
        "image": "GREEN_tire.png"
    },
    "2": {
        "id": "2",
        "type": "Slick",
        "name": "Soft",
        "color": "red",
        "description": "The red tire signifies the soft compound, designed for maximum grip and performance over shorter stints. It offers top lap times but wears out quickly, ideal for qualifying and short races.",
        "image": "RED_tire.png"
    },
    "3": {
        "id": "3",
        "type": "Slick",
        "name": "Medium",
        "color": "yellow",
        "description": "The red tire signifies the soft compound, designed for maximum grip and performance over shorter stints. It offers top lap times but wears out quickly, ideal for qualifying and short races.",
        "image": "YELLOW_tire.png"
    },
    "4": {
        "id": "4",
        "type": "Slick",
        "name": "Hard",
        "color": "white",
        "description": "The white tire, known as the hard compound, offers maximum durability and longevity, ideal for long stints and hot conditions.",
        "image": "WHITE_tire.png"
    }
}


#
#   Time Tracking
#
current_lesson = 0
lesson_timing = {
    "1": {
        "name": "Tire Types",
        "time_spent": 0,
        "lesson_start_time": 0,
        "lesson_end_time": 0,
    },
    "2": {
        "name": "Race Strategy",
        "time_spent": 0,
        "lesson_start_time": 0,
        "lesson_end_time": 0,
    },
    "3": {
        "name": "Switching Tires",
        "time_spent": 0,
        "lesson_start_time": 0,
        "lesson_end_time": 0,
    }
}

#
# home route
#
def track_time(lesson_num):
    global current_lesson
    if lesson_num == current_lesson:
        return
    
    if current_lesson != 0:
        # Calculate time spent in the previous lesson
        lesson_data = lesson_timing[str(current_lesson)]
        lesson_data["lesson_end_time"] = time.time()
        lesson_data["time_spent"] += lesson_data["lesson_end_time"] - lesson_data["lesson_start_time"]
        
        # Reset times
        lesson_data["lesson_start_time"] = 0
        lesson_data["lesson_end_time"] = 0

    if lesson_num == 0:
        return

    # Start Timer on next lesson
    current_lesson = lesson_num
    lesson_data = lesson_timing[str(current_lesson)]
    lesson_data["lesson_start_time"] = time.time()

    print(lesson_timing)

@app.route('/')
def home():
    track_time(0)
    return render_template('home.html')


#
# Space for Natal routes
#
@app.route('/learn/<lesson_num>')
def learn(lesson_num):
    if lesson_num == 1:
        tire_types()
    elif lesson_num == 2:
        race_strategy()
    else:
        switching_tires()

def tire_types():
    track_time(1)
    return render_template('tire_types.html', tire_info=tire_info)


def race_strategy():
    track_time(2)
    return render_template('race_strategy.html')


def switching_tires():
    track_time(3)
    return render_template('switching_tires.html')


#
# quiz_start route
#
@app.route('/quiz_start', methods=['GET', 'POST'])
def quiz_start():
    track_time(0)
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

            is_correct = selected_answer.lower(
            ) == question['correct'].strip().lower()

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
