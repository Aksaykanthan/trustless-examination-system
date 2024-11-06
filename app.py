from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import time

from functionalities.create_questions import addIds
from functionalities.exam_cell import final_format, get_questions

app = Flask(__name__)

# Store organizer names and their questions
organizers = {}

@app.route('/')
def index():
    global T
    T = 0 
    return render_template('index.html')

@app.route('/organizers', methods=['POST', 'GET'])
def organizers_page():
    if request.method == 'POST':
        num_organizers = int(request.form['num_organizers'])
        for i in range(1, num_organizers + 1):
            organizers[i] = {"name": f"Organizer {i}", "questions": []}
        return redirect(url_for('show_organizers'))
    return render_template('organizers.html', organizers=organizers)

@app.route('/show_organizers', methods=['GET'])
def show_organizers():
    return render_template('organizers.html', organizers=organizers)

@app.route('/update_name/<int:organizer_id>', methods=['POST', 'GET'])
def update_name(organizer_id):
    if request.method == 'POST':
        new_name = request.form['new_name']
        organizers[organizer_id]["name"] = new_name
        return redirect(url_for('show_organizers'))
    return render_template('update_name.html', organizer_id=organizer_id)

# Path to store question data
QUESTIONS_FILE_PATH = 'live_data/questions.json'

def load_json(url):
    with open(url, 'r') as file:
        return json.load(file)

def load_questions(organizer_id):
    """Load questions from JSON file for a specific organizer."""
    if os.path.exists(QUESTIONS_FILE_PATH):
        with open(QUESTIONS_FILE_PATH, 'r') as file:
            all_questions = json.load(file)
            return all_questions.get(str(organizer_id), [])
    return []

def save_questions(organizer_id, questions):
    """Save questions to JSON file under a specific organizer ID."""
    if os.path.exists(QUESTIONS_FILE_PATH):
        with open(QUESTIONS_FILE_PATH, 'r') as file:
            all_questions = json.load(file)
    else:
        all_questions = {}

    all_questions[str(organizer_id)] = questions
    with open(QUESTIONS_FILE_PATH, 'w') as file:
        json.dump(all_questions, file, indent=4)

@app.route('/add_questions/<int:organizer_id>', methods=['GET', 'POST'])
def add_questions(organizer_id):
    if request.method == 'POST':
        questions = request.json.get("questions", [])
        save_questions(organizer_id, questions)
        return jsonify({"message": "Questions saved successfully!"})

    existing_questions = load_questions(organizer_id)
    return render_template('add_questions.html', organizer_id=organizer_id, questions=existing_questions)

def format_questions():
    with open(QUESTIONS_FILE_PATH, 'r') as file:
        all_questions = json.load(file)

    for keys,values in all_questions.items():
        for i in range(len(values)):
            all_questions[keys][i] = addIds(values[i])

    with open("live_data/QuestionPaper.json", 'w') as file:
        json.dump(all_questions, file, indent=4)

    orgs = final_format(all_questions)
    return orgs

@app.route('/backend')
def backend():
    organisers = format_questions()
    get_questions(organisers)
    return render_template('backend.html')

@app.route('/questions')
def questions():
    return render_template('display_json.html', title="Questions", json_url="/questions_data")

@app.route('/questions_data')
def questions_data():
    return jsonify(load_json("live_data/questions.json"))

@app.route('/questions_with_ID')
def questions_with_id():
    return render_template('display_json.html', title="Questions with ID", json_url="/questions_with_ID_data")

@app.route('/questions_with_ID_data')
def questions_with_ID_data():
    return jsonify(load_json("live_data/QuestionPaper.json"))

@app.route('/organisers_json')
def organisers():
    return render_template('display_json.html', title="Organisers", json_url="/organisers_data")

@app.route('/organisers_data')
def organisers_data():
    return jsonify(load_json("live_data/organisers.json"))

@app.route('/encrypted_questions')
def encrypted_questions():
    return render_template('display_json.html', title="Encrypted Questions", json_url="/encrypted_questions_data")

@app.route('/encrypted_questions_data')
def encrypted_questions_data():
    return jsonify(load_json("live_data/EncryptedQuestions.json"))

if __name__ == '__main__':
    app.run(debug=True,port=3000)