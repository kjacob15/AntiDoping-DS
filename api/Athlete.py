from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for, send_from_directory
import os
from datetime import date
from extensions import db
from Models.athlete import Athlete


athlete = Blueprint('athlete', __name__)

@athlete.route('/register_athlete', methods=['POST'])
def register_athlete():
    
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