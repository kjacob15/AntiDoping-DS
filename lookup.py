from pymongo import MongoClient
from extensions import db
def test():
    db['audit'].aggregate(# audit collection aggregate to athlete colletion
        {
            '$lookup':{
                'from': 'athlete',#from athlete collection
                'localField':'athlete_location',#look up the two collections on the fields have the same value
                'foreignField':'audit_location',# athlete_location == audit_location
                'as':'new_doc' # add a new field to the audit collection
            }# the athlete collection will be in the new_doc field
        }
    )
    '''
    return {
        'athlete_email': 'xx',
        'password':'xx',
        'athlete_location':'xx',
        'time':'xx'
        'new_doc':[ 
            {'audit_email':'xx', 'password':'xx', 'audit_location':'xx'} 
     ]
     .
     .
     .
    '''



    db['audit'].aggregate(
        {
            '$lookup': {
                'from': 'athlete',
                'localField': 'athlete_location',
                'foreignField': 'audit_location',
                'as': 'new_doc'
            }
        }, {
            '$project': {
                'audit_email': 'xxx@gmail.com'
            }
        }
    )
    '''
    return  {'audit_email':'xxx@gmail.com'}
    '''
