"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    following = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.follower_id",
                             secondaryjoin="User.username==Follower.following_id")
    
    followers = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.following_id",
                             secondaryjoin="User.username==Follower.follower_id",
                             overlaps="following")
    def __repr__(self):
        print("@" + self.username)


class Follower(Base):
    __tablename__ = "followers"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    follower_id = Column('follower_id', TEXT, ForeignKey('users.username'))
    following_id = Column('following_id', TEXT, ForeignKey('users.username'))

class Tweet(Base):
    # TODO: Complete the class
    __tablename__ = "Tweets"

    id = Column("id", INTEGER, primary_key = True)
    content = Column("content", TEXT, nullable = False)
    timestamp = Column("timestamp", TEXT, nullable = False)
    username = Column("username", TEXT, nullable = False)
    

    def __init__(self, content, timestamp, username):
        self.content = content
        self.timestamp = timestamp
        self.username = username

    def __repr__(self):
        print("@" + self.username + "/n " + self.content + "/n" + self.tag)
        
class Tag(Base):
    # TODO: Complete the class
    __tablename__ = "Tags"

    id = Column("id", INTEGER, primary_key = True)
    content = Column("content", TEXT, nullable = False)

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        print("#" + self.content)
    

class TweetTag(Base):
    # TODO: Complete the class
    __tablename__ = "TweetTags"

    id = Column("id", INTEGER, primary_key = True)
    tweet_id = Column("tweet_id", INTEGER, ForeignKey('Tweet.id'))
    tag_id = Column("tag_id", INTEGER, ForeignKey('Tag.id'))
    tag = relationship("tag", back_populates = "TweetTags")
    tweet = relationship("tweet", back_populates = "TweetTags")

    def __init__(self, tweet_id, tag_id):
        self.tweet_id = tweet_id
        self.tag_id = tag_id
