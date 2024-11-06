import json
from typing import List
import uuid
import random
import os
import base64 
from functionalities.shamirs_secret import ShamirSecret, reconstruct_secret
from functionalities.symmetric_encrypt import do_encrypt, encrypt, decrypt


class Organisers:
    def __init__(self, centre_name,path="data/organisers.json"):
        self.id = uuid.uuid4().hex
        self.centre_name = centre_name
        self.key = 0
        self.keys = []
        self.addOrganiser(path)

    def addOrganiser(self,path):
        self.Organisers = path
        self.append_to_json(self.Organisers, {"id": self.id, "name": self.centre_name, "keys": [],"key":""})

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
    
    def final_addQuestions(self,questions):
        self.questions = questions

        for question in self.questions:
            quest = self.encrypt(question)
            Question_Path = "live_data/EncryptedQuestions.json"
            self.append_to_json(Question_Path, quest)

    def encrypt(self, question):
        q = {}
        if self.key == 0:
            encrypted_question, self.key = do_encrypt(question["question"], self.id)
            q["question"] = self.encode_to_string(encrypted_question)
            print("keyedd\n")
            print(self.key)
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

    def getQuestions(self,path="data/"):
        with open(path+"EncryptedQuestions.json", 'r') as f:
            questions = json.load(f)

        Path = path+"DecryptedQuestions.json"
        for question in questions:
            if question["center"] == self.centre_name:
                question["question"] = decrypt(self.decode_from_string(question["question"]), self.key)
                for option in question["options"]:
                    option["option"] = decrypt(self.decode_from_string(option["option"]), self.key)

                self.append_to_json(Path, question)
        return questions

    def do_shamir(self, path="data/organisers.json"):
        with open(path) as f:
            organisers = json.load(f)

        self.organisers_count = len(organisers)
        key_as_int = int.from_bytes(self.key, byteorder='big')
        
        shares = ShamirSecret(key_as_int, self.organisers_count, int(3 / 4 * self.organisers_count))

        for i in range(self.organisers_count):
            organisers[i]["keys"].append({"centre": self.centre_name, "share": shares[i]})
        
        with open(path, 'w') as f:
            json.dump(organisers, f, indent=4)

    def decrypt_with_shamir(self, path="data/"):
        with open(path+"organisers.json", 'r') as f:
            organisers = json.load(f)

        shares = []
        for organiser in organisers:
            for key in organiser["keys"]:
                if key["centre"] == self.centre_name:
                    shares.append(key["share"])

        if len(shares) >= int(3 / 4 * self.organisers_count):
            reconstructed_key_int = reconstruct_secret(shares)
            
            # Convert the reconstructed integer back to bytes, ensuring 32 bytes (for AES-256)
            reconstructed_key_bytes = reconstructed_key_int.to_bytes(32, byteorder='big')
            self.key = reconstructed_key_bytes  # Update key with the reconstructed byte key

            # Now decrypt questions for this center
            self.getQuestions(path)
        else:
            print(f"Not enough shares to decrypt questions for {self.centre_name}.")

    def do_shamir_final(self, path="data/organisers.json"):
        with open(path) as f:
            organisers = json.load(f)

        self.organisers_count = len(organisers)
        
        # Split the 32-byte key into 4 chunks of 8 bytes each
        chunks = [self.key[i:i+8] for i in range(0, len(self.key), 8)]
        all_shares = []
        
        # Generate shares for each chunk
        for chunk in chunks:
            chunk_int = int.from_bytes(chunk, byteorder='big')
            shares = ShamirSecret(chunk_int, self.organisers_count, int(3/4 * self.organisers_count))
            all_shares.append(shares)
        
        # Reorganize shares for each organizer
        for i in range(self.organisers_count):
            organizer_shares = [shares[i] for shares in all_shares]
            organisers[i]["keys"].append({
                "centre": self.centre_name,
                "shares": organizer_shares
            })
        
        with open(path, 'w') as f:
            json.dump(organisers, f, indent=4)

    def decrypt_with_shamir_final(self, path="data/"):
        with open(path+"organisers.json", 'r') as f:
            organisers = json.load(f)

        # Collect all shares for each chunk
        chunk_shares = [[] for _ in range(4)]  # 4 chunks
        for organiser in organisers:
            for key in organiser["keys"]:
                if key["centre"] == self.centre_name:
                    for i, share in enumerate(key["shares"]):
                        chunk_shares[i].append(share)

        if all(len(shares) >= int(3/4 * self.organisers_count) for shares in chunk_shares):
            # Reconstruct each chunk
            reconstructed_chunks = []
            for shares in chunk_shares:
                chunk_int = reconstruct_secret(shares)
                chunk_bytes = chunk_int.to_bytes(8, byteorder='big')
                reconstructed_chunks.append(chunk_bytes)
            
            # Combine chunks back into the key
            self.key = b''.join(reconstructed_chunks)
            print(f"Original key: {self.key}")
            print(f"Reconstructed key: {self.key}")
            
            self.getQuestions(path)
        else:
            print(f"Not enough shares to decrypt questions for {self.centre_name}.")

def final_format(data):
    organisers = []

    for keys,values in data.items():
        org = Organisers(keys,"live_data/organisers.json")
        org.final_addQuestions(values)
        organisers.append(org)

    for organiser in organisers:
        organiser.do_shamir_final("live_data/organisers.json")

    return organisers

def get_questions(organisers:List[Organisers]):
    for organiser in organisers:
        organiser.decrypt_with_shamir_final("live_data/")


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
    
        
    for organiser in organisers:
        organiser.do_shamir()

    # Attempt to decrypt questions for each organiser using shares
    for organiser in organisers:
        organiser.decrypt_with_shamir()
