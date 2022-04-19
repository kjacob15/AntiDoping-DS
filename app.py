from tkinter import E
from constants import EU_COUNTRY, FLASK_HOSTNAME, FLASK_PORT, REDIS_HOST, REDIS_PORT
from datetime import date, datetime
import os
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from Models.athlete import Athlete
from Models.ado import ADO
from extensions import db
# from api.Landingpage import landingPage
# from api.Athlete import athlete



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET', 'POST'])
def add():
    return render_template('add.html')

@app.route('/cancel', methods=['GET', 'POST'])
def cancel():
    return render_template('cancel.html')


@app.route('/modify', methods=['GET', 'POST'])
def modify():
    return render_template('modify.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/register_athlete', methods=['POST'])
def register_athlete():
    
    response = {}

    try:
        today = date.today()
        # timestamp = date.now()

        email_ = request.form['email']
        name_ = request.form['name']
        region= request.form['region']
        location_ = request.form['location']
        time_= request.form['time']
        date_ = request.form['date']

        if(datetime.strptime(date_,"%d/%m/%Y").date() <  today):
            response['status'] = 400
            response['message'] = 'Date has to be today or later'
            return jsonify(response) 

        if(region=='EU'):
            athlete_collection = db['EU_athlete']
        else:
            athlete_collection = db['US_athlete']

        values= athlete_collection.find({ "email": { "$eq": email_} })
        if(len(list(values))>0):
            response['status'] = 400
            response['message'] = 'Athlete entry already exists'
            return jsonify(response)

        new_athlete = Athlete(email=email_, name=name_, location=location_, date=date_, time=time_).make_dict()
        athlete_collection.insert_one(new_athlete)

        response['status'] = 200
        response['message'] = 'Athlete registered successfully'
        return jsonify(response)

    except Exception as e:
        print(e)
        response['status'] = 400
        response['message'] = 'Athlete could not be registered'
        return jsonify(response)

#POST API to delete athlete info
@app.route('/delete_athlete', methods=["POST"])
def deleteAthlete():

    response = {}

    try:
        email_ = request.form['email']

        location = request.args.get('location')
        print(location)
        if str(location) in EU_COUNTRY:
            print("YEs")
            athlete_collection = db['EU_athlete']
        else:
            print("No")
            athlete_collection = db['US_athlete']
        
        query = {"email":email_}
        values = athlete_collection.find(query)
        print(values[0])
        print("I came here 4")
        for i in values:
            print("I came here 5")
            print(i)
            athlete_collection.delete_one(i)
        

        response['status'] = 200
        response['message'] = 'Athelete deleted successfully'
        return jsonify(response)

    except Exception as e:
        print(e)
        response['status'] = 400
        response['message'] = 'Athelete could not be deleted'
        return jsonify(response)

#POST API to Modify the athlete availability
@app.route('/edit_availability', methods=["POST"])
def edit_availability():

    response = {}
    
    try:
        email_ = request.form['email']
        time_=request.form['time']
        location = request.args.get('location')
        print(location)
        if str(location) in EU_COUNTRY:
            print("YEs")
            athlete_collection = db['EU_athlete']
        else:
            print("No")
            athlete_collection = db['US_athlete']

        query = {"email":email_}
        values= athlete_collection.find(query)
        if values[0]["isAuditAssigned"] == True:
            response['status'] = 400
            response['message'] = 'Athelete update FAILED- Tester has been assigned'
            return jsonify(response)
        
        newvalues = { "$set": { "time": time_, "isAuditAssigned":False } }
        athlete_collection.update_one(values[0], newvalues)

        response['status'] = 200
        response['message'] = 'Athelete availability updated'
        return jsonify(response)

    except Exception as e:
        print(e)
        response['status'] = 400
        response['message'] = 'Athelete update FAILED'
        return jsonify(response)

#GET API to find all athletes in a region
@app.route('/find_athletes_loc', methods=['GET'])
def find_athletes_loc():
    response={}
    try:
        
        location = request.args.get('location')
        if(location in EU_COUNTRY):
             athlete_collection = db['EU_athlete']
        else:
             athlete_collection = db['US_athlete']
        
 
        # Query the DB
        athletes = athlete_collection.find({"location": location})
        athletes_info = {}

        count = 0
        for athlete in athletes:
            count += 1
            athlete_info = {}
            athlete_info['email'] = athlete['email']
            athlete_info['name'] = athlete['name']
            athlete_info['location'] = athlete['location']
            athlete_info['date'] = athlete['date']
            athlete_info['time'] = athlete['time']
            athlete_info['Tester Assigned'] = athlete['isAuditAssigned']
            athlete_index = 'athlete' + str(count)
            athletes_info[athlete_index] = athlete_info
        return jsonify(athletes_info)
    except Exception as e:
        print(e)
        response['message']= "Request failed" +e
        return response

#GET API to find athlete by email
@app.route('/find_athletes', methods=['GET'])
def find_athletes():
    response={}
    try:
        
        email_ = request.args.get('email')
        location = request.args.get('location')

        if(location in EU_COUNTRY):
             athlete_collection = db['EU_athlete']
        else:
             athlete_collection = db['US_athlete']

        # if(not email_):
        #     email_=""

        # Query the DB
        athletes = athlete_collection.find({"email": email_})
        athletes_info = {}

        count = 0
        for athlete in athletes:
            count += 1
            athlete_info = {}
            athlete_info['email'] = athlete['email']
            athlete_info['name'] = athlete['name']
            athlete_info['location'] = athlete['location']
            athlete_info['date'] = athlete['date']
            athlete_info['time'] = athlete['time']
            athlete_index = 'athlete' + str(count)
            athletes_info[athlete_index] = athlete_info
        return jsonify(athletes_info)
    except Exception as e:
        print(e)
        response['message']= "Request failed" +e
        return response

@app.route('/istestassigned', methods=['GET'])
def istestassigned():
    response={}
    try:
        
        email_ = request.args.get('email')
        location = request.args.get('location')

        if(location in EU_COUNTRY):
             athlete_collection = db['EU_athlete']
        else:
             athlete_collection = db['US_athlete']

        # if(not email_):
        #     email_=""

        # Query the DB
        athletes = athlete_collection.find({"email": email_})
        athletes_info = {}

        count = 0
        for athlete in athletes:
            count += 1
            athlete_info = {}
            athlete_info['email'] = athlete['email']
            athlete_info['name'] = athlete['name']
            athlete_info['location'] = athlete['location']
            athlete_index = 'athlete' + str(count)
            if(athlete["isAuditAssigned"]==True):
                athletes_info["Tester_Assigned"]= "Yes"
            else:
                athletes_info["Tester_Assigned"]= "No"
            athletes_info[athlete_index] = athlete_info
        return jsonify(athletes_info)
    except Exception as e:
        print(e)
        response['message']= "Request failed" +e
        return response


@app.route('/register_ado', methods=['POST'])
def register_ado():
    
    response = {}

    try:

        email_ = request.form['email']
        location_ = request.form['location']

        ado_collection = db['ADO']

        values= ado_collection.find({ "email": { "$eq": email_} })
        if(len(list(values))>0):
            response['status'] = 400
            response['message'] = 'Athlete entry already exists'
            return jsonify(response)

        new_ado = ADO(email=email_, location=location_).make_dict()
        ado_collection.insert_one(new_ado)

        response['status'] = 200
        response['message'] = 'ADO registered successfully'
        return jsonify(response)

    except Exception as e:
        print(e)
        response['status'] = 400
        response['message'] = 'ADO could not be registered'
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host=FLASK_HOSTNAME, port=FLASK_PORT)