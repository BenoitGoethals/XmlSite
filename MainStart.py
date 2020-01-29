import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
import csv
import requests
import feedparser as FP
from flask import render_template
import flask
import random
from datetime import date
from datetime import datetime
from datetime import time
import webbrowser
import os

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.pool import SingletonThreadPool


def readCSV():
    data = set()
    with open('rsslinks.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            data.add(LinkSite(row[0], row[1], row[2]))

    return data


def parseXML(xml):
    # create element tree object
    el = FP.parse(xml)

    # create empty list for news items
    newsitems = []
    for entry in el.entries:
        news = News( entry.published, entry.summary, entry.title)
        newsitems.append(news)
        # return news items list
    return newsitems


def getDataFromURL(url):
    # creating HTTP response object from given url
    resp = requests.get(url)

    return resp.text


def makeHtml(channel, newsBulk):
    import os
    folder = str(date.today())
    if not os.path.exists(folder):
        os.makedirs(folder)

    app = flask.Flask('my app')
    file = ".\\" + folder + "\\" + channel + str(datetime.now()).replace(" ", "").replace(".", "").replace(":",
                                                                                                           "") + ".html"
    with app.app_context():
        rendered = render_template('index.html', \
                                   title="News " + channel + " " + str(date.today()), \
                                   news=newsBulk)

        f = open(file, 'wb')

        f.write(str.encode(rendered))
        f.close()
        webbrowser.open_new_tab(file)


Base = declarative_base()


class LinkSite(Base):
    __tablename__ = 'linkSite'
    id = Column(Integer, primary_key=True)
    channel = Column(String(250),unique=False)
    theme = Column(String(250))
    url = Column(String(250))

    def __init__(self, channel, theme, url):
        self.channel = str.strip(channel)
        self.theme = str.strip(theme)
        self.url = str.strip(url)

    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])

    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    published = Column(String(250))
    summary = Column(String(250))
    title = Column(String(250))
    linkSite_id = Column(Integer, ForeignKey('linkSite.id'))
    linkSite = relationship(LinkSite, backref=backref('newses', uselist=True))

    def __init__(self, published, summary, title):
        self.published = str.strip(published)
        self.summary = str.strip(summary)
        self.title = title

    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])

    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])

def get_or_create(session, model, defaults=None, **kwargs):
	"""
	Get or create a model instance while preserving integrity.
	"""
	try:
		return session.query(model).filter_by(**kwargs).one(), False
	except NoResultFound:
		if defaults is not None:
			kwargs.update(defaults)
		try:
			with session.begin_nested():
				instance = model(**kwargs)
				session.add(instance)
				return instance, True
		except IntegrityError:
			return session.query(model).filter_by(**kwargs).one(), False
def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval',seconds=5)
    scheduler.start()

    a=input("return to stop")

def job():
    print("hello")

    engine = create_engine('sqlite:///store.db', poolclass=SingletonThreadPool)
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker()
    session.configure(bind=engine)
    connection = engine.connect()


    import glob
    s = session()
    mylist = [f for f in glob.glob("*.html")]
    for f in mylist:
        os.remove(f)

    data = readCSV()
    if data is not None:
        for url in data:
         #  ls=get_or_create(s , LinkSite, defaults=None, url=url.url)
         try:
            ls=s.query(LinkSite).filter_by(url=url.url).one()
            url = ls
         except NoResultFound:
            s.add(url)


        result: str = getDataFromURL((url.url))
        if result is not None:
              #  print(result)
          news = parseXML(result)
          for newsLine in news:
              try:
                  s.query(News).filter_by(title=newsLine.title).one()

              except NoResultFound:
                newsLine.linkSite = url
                s.add(newsLine)
            #   makeHtml(url.channel, news)

    s.commit()

    print(s.query(News).order_by(News.id).count())
   # i=0
   # for instance in s.query(News).order_by(News.id):
    #    i=i+1
     #   print(i)
      #  print(instance.id)
       # print(instance.title)
    #    print( instance.summary)
     #   print(instance.linkSite.channel)

    print(s.query(LinkSite).count())
  #  for instance2 in s.query(LinkSite):
   #     print(instance2.id)
    #    print(instance2.channel)
     #   print(instance2.url)


if __name__ == "__main__":
    main()
