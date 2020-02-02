import csv
import requests
import feedparser as FP
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import render_template
import flask
import random
from datetime import date
from datetime import datetime
from datetime import time
import webbrowser
import os
from flask import Flask, jsonify
from flask import abort
from flask import make_response
import json

from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
import csv

import feedparser as FP
from flask import render_template
import flask
from datetime import date
from datetime import datetime
import webbrowser
import os
import platform
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.pool import SingletonThreadPool
import logging

from Entitys import Base, LinkSite, News



def __getWheather(city,link):
    headers = {'Content-Type': 'application/json'}


    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def get_weather(city):
    api_url_base = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + "&units=metric&lang=nl&APPID=8434e7589baa7da22d0220b2669daef0"
    return __getWheather(city,api_url_base)


def get_weatherForCast(city):
    api_url_base = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + "&units=metric&lang=nl&APPID=8434e7589baa7da22d0220b2669daef0"
    print(api_url_base)
    return __getWheather(city, api_url_base)




def make_Html(newsBulk):
    import os
    print("generate")
    folder = str(date.today())
    if not os.path.exists(folder):
        os.makedirs(folder)

    app = flask.Flask('my app')

    responseWeather = get_weather("dendermonde")
    if platform.system() == 'Windows':
        file = os.path.join(".", folder, 'index.html')
    else:
        file = '/var/www/html/index.html'
    # file = "./" + folder + "/index.html"
    with app.app_context():
        rendered = render_template('index.html', \
                                   title="News " + " " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), \
                                   news=newsBulk,weather=responseWeather['weather'][0]['description'],temperatuur=responseWeather['main']['temp'])

        f = open(file, 'wb')

        f.write(str.encode(rendered))
        f.close()
        # webbrowser.open_new_tab(file)


def get_Data():
    engine = create_engine('sqlite:///store.db', poolclass=SingletonThreadPool)
    print("job running")
    Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker()
    session.configure(bind=engine)
    connection = engine.connect()
    s = session()

    today = datetime.now().strftime("%Y-%m-%d")
    try:

        data = s.query(News).filter(News.published.like(today + "%")).all()
        #   data = s.query(News).filter(published = today).all()

        if len(data) == 0:
            session.close_all
            connection.close()
            return None
        session.close_all
        connection.close()
        return [
            {'id': n.id, 'summary': n.summary, 'title': n.title, 'url': n.linkSite.channel} for n in
            data]
    except NoResultFound:
        session.close_all
        connection.close()
        return None


def job():
    data = get_Data()
    if data != None:
        make_Html(data)


def main():
    print("start")
    logging.basicConfig(filename='htmlgenerator.log', level=logging.INFO)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', seconds=30)
    scheduler.start()

    a = input("return to stop")


if __name__ == "__main__":
    main()
