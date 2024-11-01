import random
import json
import datetime

from create_ledger import *
from RSA import decrypt_with_key

def simulate_exam():
    question_bank = Questions("data/QuestionPaper.json",10)

    # Setting Start Time and End Time
    startTime = datetime.datetime.now()
    endTime = startTime + datetime.timedelta(minutes=30)

    #Initializing Ledger
    ledger = Ledger(startTime,endTime)
    students = Students("data/students.json")

    # Simulating Exam
    for i in range(10):
        student = random.choice(students.students)
        question = random.choice(question_bank.questions)
        option = random.choice(question["options"])
        response = Response(student["id"],question["questionId"],option["optionId"])
        ledger.addResponse(response,students,question_bank)

    with open("ledger.json",'w') as f:
        json.dump(ledger.ledger,f)


def decrypting_ledger():
    with open("data/ledger.json",'r') as f:
        ledger = json.load(f)
        l = []
        for response in ledger:
            r = Response.decrypt(response)
            l.append(r)

        
    with open("data/decrypted_ledger.json",'w') as f:
        json.dump(l,f)

if __name__ == '__main__':
    # simulate_exam()
    decrypting_ledger()