from datetime import date
import os
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from Models.athlete import Athlete
from extensions import db
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

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
def registerAthlete():
    
    response = {}

    try:
        today = date.today()
        # timestamp = date.now()

        email_ = request.form['email']
        name_ = request.form['name']
        location_ = request.form['location']
        time_= request.form['time']
        date_ = today.strftime("%d/%m/%Y")


        athlete_collection = db['athlete']


        query = {"email":email_}
        values= athlete_collection.find({ "email": { "$eq": email_} })
        if(len(list(values))>0):
            response['status'] = 400
            response['message'] = 'Athlete entry already exists'
            return jsonify(response)


        new_athlete = Athlete(email=email_, name=name_,
                              location=location_, date=date_, time=time_).make_dict()
        athlete_collection.insert_one(new_athlete)

        response['status'] = 200
        response['message'] = 'Athlete registered successfully'
        return jsonify(response)

    except Exception as e:
        print(e)
        response['status'] = 400
        response['message'] = 'Athlete could not be registered'
        return jsonify(response)



if __name__ == '__main__':
   app.run()