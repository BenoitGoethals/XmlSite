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
    newsitems    = []
    for entry in el.entries:
        news=News(entry.id,entry.published,entry.summary,entry.title)
        newsitems.append(news)
        # return news items list
    return newsitems

def getDataFromURL(url):
    # creating HTTP response object from given url
    resp = requests.get(url)

    return resp.text




def makeHtml(channel,newsBulk):
    import os
    folder = str(date.today())
    if not os.path.exists(folder):
        os.makedirs(folder)

    app = flask.Flask('my app')
    file=".\\" + folder + "\\" +channel+str(datetime.now()).replace(" ","").replace(".","").replace(":","")+".html"
    with app.app_context():
        rendered = render_template('index.html', \
                                   title="News "+channel+" "+str(date.today()), \
                                   news=newsBulk)


        f = open(file, 'wb')



        f.write(str.encode(rendered))
        f.close()
        webbrowser.open_new_tab(file)

class News():

    def __init__(self,id,published,summary,title):
        self.id=str.strip(id)
        self.published=str.strip(published)
        self.summary=str.strip(summary)
        self.title=title

    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])

    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])



class LinkSite:

    def __init__(self,channel,theme,url):
        self.channel=str.strip(channel)
        self.theme=str.strip(theme)
        self.url=str.strip(url)

    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])

    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])


def main():
    import glob

    mylist = [f for f in glob.glob("*.html")]
    for f in mylist:
        os.remove(f)

    data=readCSV()
    if data is not None:
        for url in data:
            result= getDataFromURL((url.url))
            if result is not None:
              #  print(result)
                news=parseXML(result)
                makeHtml(url.channel, news)


if __name__ == "__main__":
    main()
