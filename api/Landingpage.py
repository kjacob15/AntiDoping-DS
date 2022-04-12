from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for, send_from_directory
import os


landingPage = Blueprint('landingPage', __name__)

@landingPage.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@landingPage.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(landingPage.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@landingPage.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))