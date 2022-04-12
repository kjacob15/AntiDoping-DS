class Athlete():
    
    email = ''
    name = ''
    location = ''
    date=''
    time = ''
    isAuditAssigned = False

    def __init__(self, email, name, location, date, time):

        self.email = email
        self.name = name
        self.location = location
        self.date= date
        self.time = time
    
    def make_dict(self):
        athelte_info = {}
        athelte_info['email'] = str(self.email)
        athelte_info['name'] = str(self.name)
        athelte_info['location'] = str(self.location)
        athelte_info['date'] = str(self.date)
        athelte_info['time'] = str(self.time)
        
        return athelte_info
