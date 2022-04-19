class ADO:
    email = ''
    name = ''
    location = ''
    assigned_athletes = []

    def __init__(self, email, location):
        self.email = email
        self.location = location
        self.assigned_athletes = []

    def make_dict(self):
        audit_info = {}
        audit_info['email'] = self.email
        audit_info['location'] = self.location
        audit_info['assigned_athletes'] = self.assigned_athletes
        return audit_info

    # Mohammad, make the required changes here
    def assign_athlete(self, athlete):
        athlete_info = {'email': str(athlete.email),
                        'time': str(self.time)}
        self.assigned_athletes.append(athlete_info)
