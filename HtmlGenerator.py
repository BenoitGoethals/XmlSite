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


def make_Html(newsBulk):
    import os
    folder = str(date.today())
    if not os.path.exists(folder):
        os.makedirs(folder)

    app = flask.Flask('my app')
    file= os.path.join(".",folder, 'index.html')
   # file = "./" + folder + "/index.html"
    with app.app_context():
        rendered = render_template('index.html', \
                                   title="News " + " " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), \
                                   news=newsBulk)

        f = open(file, 'wb')

        f.write(str.encode(rendered))
        f.close()
        # webbrowser.open_new_tab(file)


def get_Data():
    engine = create_engine('sqlite:///store.db', poolclass=SingletonThreadPool)

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
            return None

        return [
            {'id': n.id, 'summary': n.summary, 'title': n.title, 'url': n.linkSite.channel} for n in
            data]
    except NoResultFound:
        return None


def job():
    data = get_Data()
    if data != None:
        make_Html(data)


def main():
    logging.basicConfig(filename='htmlgenerator.log', level=logging.INFO)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', minutes=1)
    scheduler.start()

    a = input("return to stop")


if __name__ == "__main__":
    main()
