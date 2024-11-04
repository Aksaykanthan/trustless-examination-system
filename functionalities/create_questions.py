import json
import uuid


def addIds(question):
    
    options =  list(map(lambda x:  {"option" : x, "optionId" : uuid.uuid4().hex},question['options']))
    answer = list(filter(lambda x: x['option'] == question['answer'], options))[0]
    return {
        "questionId" : uuid.uuid4().hex,
        "question" : question['question'],
        "options" : options,
        "answer" : answer['optionId']
    }

def generate_questions(data):
    return  [
        addIds(x) for x in data
    ]

def save(questions):
    with open("data/QuestionPaper.json",'w') as f:
        json.dump(questions,f)
    print("saved sucessfully")

if __name__ == "__main__":
    with open("data/questions.json") as f:
        data = json.load(f)

    questions = generate_questions(data)
    save(questions)
