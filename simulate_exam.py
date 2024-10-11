import json
import random
import datetime

class Response:
    def __init__(self,userId,questionId,optionId):
        self.userId = userId
        self.questionId = questionId
        self.optionId = optionId
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return f"UserId : {userId}\nQuestionId : {questionId}\nOptionId : {optionId}\nTime : {timestamp}"

    def encrypt(self):
        return self


class Ledger:
    def __init__(self,startTime,endTime):
        self.ledger = []
        self.startTime = startTime
        self.endTime = endTime

    def addResponse(self, response:Response):
        currentTime = datetime.datetime.now()
        if self.startTime < currentTime and self.endTime > currentTime:
            # check valide Student, questionId, optionId 
            # If not valide report
            self.ledger.append(response.encrypt())
            return {"response" : "Response Added Successfully"}
                
        return {"response" : "TimeOut"}
            

class Students:
    def __init__(self,data_path:String):
        self.data_path = data_path
        with open(datapath) as f:
            students = json.load(f)

        self.students = students
        self.no_of_students = len(students)
    
    def verify_student(self,studentId):
        # check if the studentID is stored in the database
        return True if self.getStudentById(studentID) else False

    def getStudentById(self,studentId):
        ...



with open("data/questions.json") as f:
    questions = json.load(f)
    questions = questions[:10]


NO_OF_STUDENT=4






