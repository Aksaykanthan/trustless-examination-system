import json
import uuid
import random
import os
import base64 
from symmetric_encrypt import do_encrypt, encrypt, decrypt
from shamirs_secret import ShamirSecret, reconstruct_secret

class Organisers:
    def __init__(self, centre_name):
        self.id = uuid.uuid4().hex
        self.centre_name = centre_name
        self.key = 0
        self.keys = []
        self.addOrganiser()

    def addOrganiser(self):
        self.Organisers = "data/organisers.json"
        self.append_to_json(self.Organisers, {"id": self.id, "name": self.centre_name, "keys": []})

        with open(self.Organisers, 'r') as f:
            organisers = json.load(f)

        self.organisers_count = len(organisers)

    def append_to_json(self, file_path, new_data):
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump([], file)

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)  
        except json.JSONDecodeError:
            data = []

        if isinstance(data, list):
            data.append(new_data)
        elif isinstance(data, dict):
            data.update(new_data)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def addQuestions(self, question_bank):
        with open("data/QuestionPaper.json", 'r') as f:
            question_bank = json.load(f)

        self.questions = random.choices(question_bank, k=10)

        for question in self.questions:
            quest = self.encrypt(question)
            Question_Path = "data/EncryptedQuestions.json"
            self.append_to_json(Question_Path, quest)

    def encrypt(self, question):
        q = {}
        if self.key == 0:
            encrypted_question, self.key = do_encrypt(question["question"], self.id)
            q["question"] = self.encode_to_string(encrypted_question)
        else:
            encrypted_question = encrypt(question["question"], self.key)
            q["question"] = self.encode_to_string(encrypted_question)

        q["questionId"] = question["questionId"]

        opt = []
        for option in question["options"]:
            encrypted_option = encrypt(option["option"], self.key)
            encrypted_str = self.encode_to_string(encrypted_option)
            opt.append({"option": encrypted_str, "optionId": option['optionId']})

        q["options"] = opt
        q["answer"] = question["answer"]
        q["center"] = self.centre_name
        return q

    def encode_to_string(self, encrypted_bytes):
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decode_from_string(self, encrypted_str):
        return base64.b64decode(encrypted_str)

    def getQuestions(self):
        with open("data/EncryptedQuestions.json", 'r') as f:
            questions = json.load(f)
        
        Path = "data/DecryptedQuestions.json"
        for question in questions:
            if question["center"] == self.centre_name:
                # Extract IV and encrypted question
                encrypted_question = self.decode_from_string(question["question"])
                decrypted_question = decrypt(encrypted_question, self.key)
                question["question"] = decrypted_question  # Update decrypted question

                for option in question["options"]:
                    encrypted_option = self.decode_from_string(option["option"])
                    decrypted_option = decrypt(encrypted_option, self.key)
                    option["option"] = decrypted_option  # Update decrypted option

                self.append_to_json(Path, question)
        return questions


    def do_shamir(self):
        # Convert the byte key to an integer before sharing it
        key_as_int = int.from_bytes(self.key, byteorder='big')
        
        shares = ShamirSecret(key_as_int, self.organisers_count, int(3 / 4 * self.organisers_count))
        
        with open("data/organisers.json") as f:
            organisers = json.load(f)
            for i in range(self.organisers_count):
                organisers[i]["keys"].append({"centre": self.centre_name, "share": shares[i]})

    def decrypt_with_shamir(self):
        # Reconstruct key from Shamir shares
        reconstructed_key_int = self.reconstruct_key_from_shares()
        # Convert the integer to 32-byte key
        self.key = reconstructed_key_int.to_bytes(32, byteorder='big')
        
        # Check key length to ensure it's 32 bytes
        assert len(self.key) == 32, "Key length should be 32 bytes"
        print("Reconstructed Key:", self.key)  # Debugging: Print to verify correct key format
        
        self.getQuestions()


if __name__ == '__main__':
    # Create 5 organizers
    organiser1 = Organisers("IIT Pallakad")
    organiser2 = Organisers("IIT Bombay")
    organiser3 = Organisers("IIT Delhi")
    organiser4 = Organisers("IIT Madras")
    organiser5 = Organisers("IIT Kanpur")

    organisers = [organiser1, organiser2, organiser3, organiser4, organiser5]

    # Add questions and apply Shamir for each organiser
    for organiser in organisers:
        organiser.addQuestions("data/QuestionPaper.json")
        organiser.do_shamir()

    # Attempt to decrypt questions for each organiser using shares
    # for organiser in organisers:
    #     organiser.decrypt_with_shamir()
