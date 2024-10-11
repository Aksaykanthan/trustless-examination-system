import json
import random
import uuid
import names

NO_OF_STUDENTS=20
filepath = 'data/students.json'

def create_student():
    return {
        "name" : names.get_full_name(),
        "id" : uuid.uuid4().hex
    }

def create_students(n):
    return [
        create_student() for _ in range(n)
    ]

def save_students(students,filepath):
    with open(filepath,"w") as f:
        json.dump(students,f)
    print("students database created successfully")

if __name__ == "__main__":
    students = create_students(NO_OF_STUDENTS)
    save_students(students,filepath)
