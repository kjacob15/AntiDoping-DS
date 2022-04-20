
from pymongo import MongoClient
from datetime import datetime
from time import sleep

connection_string = 'mongodb://cosmosdbwado:ScGN9zHoE3QG20kewxQOllNs4eMvaE7rRzKsvzgwfw87Ay4a1s2rbPFx71jEs4B3qFU0EtFnbccGRuGewfl8yw==@cosmosdbwado.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@cosmosdbwado@'

mongo_client = MongoClient(connection_string)

db = mongo_client['wado']

import threading

Regions = ['US_athlete','EU_athlete']
US_countries  = ['USA', 'Canada', 'Mexico']
ado_collection = db['ADO']
US_athlete_collection = db['US_athlete']
  
def find_athelte_in(region, location):

    response={}

    try:
        athlete_collection = db[region]

        query = {'location' : location ,'isAuditAssigned': False}
        athletes= athlete_collection.find(query)

        athletes_info = []
        for athlete in athletes:
            athlete_info = {}
            athlete_info['email'] = athlete['email']
            athlete_info['name'] = athlete['name']
            athlete_info['location'] = athlete['location']
            athlete_info['date'] = athlete['date']
            athlete_info['time'] = athlete['time']
            athlete_info['isAuditAssigned'] = athlete['isAuditAssigned']
            athletes_info.append(athlete_info)
        return athletes_info

    except Exception as e:
        print(e)
        response['message']= 'Request failed' +e
        return response

def find_ado_in(location):

    response={}

    try:
        ado_collection = db['ADO']

        query = {'location' : location, 'assigned_athletes': {"$size": 2}}
        ados_with_one_qouta  = ado_collection.find(query)

        query = {'location' : location, 'assigned_athletes': {"$size": 1}}
        ados_with_two_qouta  = ado_collection.find(query)    

        query = {'location' : location, 'assigned_athletes': {"$size": 0}}
        ados_with_three_qouta  = ado_collection.find(query)


        ados_with_one_qouta_info = []
        for ado in ados_with_one_qouta:
            ado_info = {}
            ado_info['email'] = ado['email']
            ado_info['location'] = ado['location']
            ado_info['assigned_athletes'] = ado['assigned_athletes']
            ados_with_one_qouta_info.append(ado_info)

        ados_with_two_qouta_info = []
        for ado in ados_with_two_qouta:
            ado_info = {}
            ado_info['email'] = ado['email']
            ado_info['location'] = ado['location']
            ado_info['assigned_athletes'] = ado['assigned_athletes']
            ados_with_two_qouta_info.append(ado_info)

        ados_with_three_qouta_info = []
        for ado in ados_with_three_qouta:
            ado_info = {}
            ado_info['email'] = ado['email']
            ado_info['location'] = ado['location']
            ado_info['assigned_athletes'] = ado['assigned_athletes']
            ados_with_three_qouta_info.append(ado_info)

        return ados_with_one_qouta_info + ados_with_two_qouta_info + ados_with_three_qouta_info

    except Exception as e:
        print(e)
        response['message']= 'Request failed' + e
        return response

def ado_printer(ados):
    for ado in ados:
        ado_email = ado['email']
        ado_location = ado['location']
        print('\033[0;37;40m',datetime.now(),'\033[1;36;40m', f'- ADO {ado_email} {ado_location}')
        sleep(2)

def athlete_printer(athletes):
    for athlete in athletes:
        ath_email = athlete['email']
        ath_location = athlete['location']
        ath_time = athlete['time']
        ath_date = athlete['date']
        print('\033[0;37;40m',datetime.now(),'\033[1;35;40m', f'- Athelete {ath_email} {ath_location} {ath_date} {ath_time} ')
        sleep(2)

def athlete_ado_printer(athelte, ado):
    ado_email = ado['email']
    ath_email = athelte['email']
    ath_location = athelte['location']
    ath_time = athelte['time']
    ath_date = athelte['date']
    print('\033[0;37;40m',datetime.now(), '\033[1;33;40m' ,f'- ADO {ado_email} Assigned to {ath_email} in {ath_location} {ath_date} at {ath_time}')
    sleep(2)

def time_overlap(ado,assigned_athletes ,new_athlete):

    return_value = False

    for i in range(len(ado['assigned_athletes'])):
        if ado['assigned_athletes'][i]['date'] == new_athlete['date']:
            if ado['assigned_athletes'][i]['time'] == new_athlete['time']:
                return_value = True

    for i in range(len(assigned_athletes)):
        if assigned_athletes[i]['date'] == new_athlete['date']:
            if assigned_athletes[i]['time'] == new_athlete['time']:
                return_value = True

    return return_value


def reach_quota(ado , assigned_athletes):

    return_value = False
    ado_email = ado['email']

    if len(ado['assigned_athletes']) >= 3:
        return_value = True

    if len(assigned_athletes) >= 3:
        return_value = True

    if len(ado['assigned_athletes']) + len(assigned_athletes) >= 3:
        return_value = True

    #if(return_value):
        #print('\033[1;34;40m', datetime.now(), f'ADO {ado_email} has reached its quota.')

    return return_value


def assign_ado_to_athlete(new_athlete, ado):
    newvalues = { "$set": { "isAuditAssigned" : True , "ADOId" : ado['email']  } }
    US_athlete_collection.update_one(new_athlete, newvalues)
    new_athlete['isAuditAssigned'] = True
    new_athlete['ADOId'] = ado['email']
    athlete_ado_printer(new_athlete,ado)
    sleep(2)

def already_assigned(new_athlete):
    if new_athlete['isAuditAssigned'] == True:
        return True
    return False

def update_athlete_list(assigned_athletes, ado):
    newvalues = { "$set": { "assigned_athletes": ado['assigned_athletes'] + assigned_athletes } }
    ado_collection.update_one(ado, newvalues)
    sleep(2)

def US_assigner():
    for country in US_countries:
        print('\033[1;32;40m',f'--------- {country} ---------')
        ados = find_ado_in(str(country))
        ado_printer(ados)
        athletes = find_athelte_in('US_athlete',str(country))
        len_athletes = len(athletes)
        athlete_printer(athletes)
        for ado in ados:
            assigned_athletes = []
            for i in range(len(athletes)):
                if (reach_quota(ado, assigned_athletes) == False):
                    if(time_overlap(ado,assigned_athletes ,athletes[i]) == False):
                        if(already_assigned(athletes[i]) == False):
                            assigned_athletes.append(athletes[i])
                            assign_ado_to_athlete(athletes[i], ado)
                    continue
            update_athlete_list(assigned_athletes,ado)
        print('\033[0;37;40m',datetime.now(),f'- No Athelete - ADO match Available in {country}')


if __name__ == '__main__':

    US_athlete_collection.update_many({}, {"$set" : {'isAuditAssigned': False}})
    US_athlete_collection.update_many({}, {"$set" : {'ADOId': ''}})
    ado_collection.update_many({},{"$set" : {'assigned_athletes': []}})

    count = 0
    while(1):
        count = count + 1
        print('\033[1;31;40m',f'--------- Round {count} ---------')
        US_assigner()
        sleep(20)
        