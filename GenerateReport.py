from flask import Flask, jsonify
from flask import abort
from flask import make_response

from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
import csv
import requests
import feedparser as FP
from flask import render_template
import flask
from datetime import date
from datetime import datetime
import webbrowser
import os

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.pool import SingletonThreadPool
import logging

from Entitys import Base, LinkSite, News

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@app.route('/news/<string:news>', methods=['GET'])
def get_news(news):
    print("hello")

    engine = create_engine('sqlite:///store.db', poolclass=SingletonThreadPool)
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker()
    session.configure(bind=engine)
    connection = engine.connect()
    s = session()

    try:

        data = s.query(News).join(LinkSite).filter(LinkSite.channel == news).all()

        if len(data) == 0:
            abort(404)

        return jsonify([
            {'id': book.id, 'Summary': book.summary, 'title': book.title, 'url': book.linkSite.channel } for book in data     ])
    except NoResultFound:
        return None


@auth.get_password
def get_password(username):
    if username == 'benoit':
        return 'ranger14'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})


if __name__ == '__main__':
    app.run(debug=True)
