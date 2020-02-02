from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class LinkSite(Base):
    __tablename__ = 'linkSite'
    id = Column(Integer, primary_key=True)
    channel = Column(String(250), unique=False)
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