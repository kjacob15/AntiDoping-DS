from flask import Flask, jsonify


class Athlete:
    email = ''
    name = ''
    location = ''
    date = ''
    time = ''
    isAuditAssigned = False

    def __init__(self, email, name, location, date, time):
        self.email = email
        self.name = name
        self.location = location
        self.date = date
        self.time = time

    def make_dict(self):
        athelte_info = {'email': str(self.email),
                        'name': str(self.name),
                        'location': str(self.location),
                        'date': str(self.date),
                        'time': str(self.time),
                        'isAuditAssigned': self.isAuditAssigned}
        user = {
            "ïd":"",
            "name": "",
            "email": "",
            "password": "",
            "date": "",
            "time": "",

        }
