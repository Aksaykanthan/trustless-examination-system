import json
import datetime
from RSA import start_encrypt,encrypt_with_key,decrypt_with_key

class Response:
    def __init__(self,userId,questionId,optionId):
        self.userId = userId
        self.questionId = questionId
        self.optionId = optionId
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return f"UserId : {self.userId}\nQuestionId : {self.questionId}\nOptionId : {self.optionId}\nTime : {self.timestamp}"

    def encrypt(self,resp):
        coded,private_key,public_key,n = start_encrypt(resp["UserId"])
        resp["UserId"] = coded
        resp["QuestionId"] = encrypt_with_key(resp["QuestionId"],private_key)
        resp["OptionId"] = encrypt_with_key(resp["OptionId"],private_key)
        resp["PublicKey"] = public_key
        resp["N"] = n
        return resp
    
    @staticmethod
    def decrypt(resp):
        resp["UserId"] = decrypt_with_key(resp["UserId"],resp["PublicKey"],resp["N"])
        resp["QuestionId"] = decrypt_with_key(resp["QuestionId"],resp["PublicKey"],resp["N"])
        resp["OptionId"] = decrypt_with_key(resp["OptionId"],resp["PublicKey"],resp["N"])
        return resp

    def fetch(self):
        result = {"UserId" : self.userId,"QuestionId" : self.questionId,"OptionId" : self.optionId,"Time" : str(self.timestamp)}
        encrypted = self.encrypt(result)
        return encrypted


class Students:
    def __init__(self,data_path:str):
        self.data_path = data_path
        with open(data_path) as f:
            students = json.load(f)

        self.students = students
        self.no_of_students = len(students)
    
    def verify_student(self,studentId:str):
        return True if self.getStudentById(studentId) else False

    def getStudentById(self,studentId:str):
        for student in self.students:
            if student["id"] == studentId:
                return student
        return None

class Questions:
    def __init__(self,question_path:str,length:int):
        self.question_path = question_path
        with open(question_path) as f:
            questions = json.load(f)
            self.questions = questions[:length]

    def getQuestionById(self,questionId:str):
        for question in self.questions:
            if question["questionId"] == questionId:
                return question
        return None
    
    def verify_question(self,questionId:str):
        return True if self.getQuestionById(questionId) else False
    
    def verify_option(self,questionId:str,optionID):
        question = self.getQuestionById(questionId)
        return True if any(option['optionId'] == optionID for option in question['options']) else False

class Ledger:
    def __init__(self,startTime,endTime):
        self.ledger = []
        self.startTime = startTime
        self.endTime = endTime

    def addResponse(self, response:Response, student:Students, questions:Questions): 
        # Checking Current Time 
        currentTime = datetime.datetime.now()

        if self.startTime < currentTime and self.endTime > currentTime:

            # checking existance StudentId  
            if not student.verify_student(response.userId):
                return {"response" : "Student ID Not Found"}
            
            if not questions.verify_question(response.questionId):
                return {"response" : "Question ID Not Found"}
            
            if not questions.verify_option(response.questionId,response.optionId):   
                return {"response" : "Option ID Not Found"}
            
            self.ledger.append(response.fetch())
            return {"response" : "Response Added Successfully"}
                
        return {"response" : "TimeOut"}
            

