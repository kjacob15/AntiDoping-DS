class ADO():
    
    email = ''
    name = ''
    location = ''
    assigned_athletes = []

    def __init__(self, email, name, location):
        self.email = email
        self.name = name
        self.location = location
        self.assigned_athletes = []
    
    def make_dict(self):
        audit_info = {}
        audit_info['email'] = self.email
        audit_info['name'] = self.name
        audit_info['location'] = self.location
        audit_info['assigned_athletes'] = self.assigned_athletes
        return audit_info
    
    #Mohammad, make the required changes here
    def assign_athlete(self, athlete):
        athlete_info = {}
        athlete_info['email'] = str(athlete.email)
        athlete_info['time'] = str(self.time)
        self.assigned_athletes.append(athlete_info)