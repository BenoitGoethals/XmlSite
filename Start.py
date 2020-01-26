import csv
import requests
import feedparser as FP

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
        news=News(entry.id,entry.published,entry.summary)
        newsitems.append(news)
        # return news items list
    return newsitems

def getDataFromURL(url):
    # creating HTTP response object from given url
    resp = requests.get(url)

    return resp.text





def makeHtml():
    pass

class News():

    def __init__(self,id,published,summary):
        self.id=str.strip(id)
        self.published=str.strip(published)
        self.summary=str.strip(summary)

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
    data=readCSV()
    if data is not None:
        for url in data:
            result= getDataFromURL((url.url))
            if result is not None:
                print(result)
                news=parseXML(result)
                for n in news:
                    print(n)







if __name__ == "__main__":
    main()
