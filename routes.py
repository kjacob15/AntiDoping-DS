from functools import wraps

from flask import Flask, request
from app import app
from Models.athlete import Athlete


def res(func):
    @wraps(func)
    @app.route('/signup', methods=['POST'])
    def signup():
        if request.method == "POST":
            if request.get_json()["user"]:
                response = "ok"
                return Athlete().make_dict()
