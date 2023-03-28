from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    """
    The menu to print once a user has logged in
    """
    def __init__(self, curr_user = None, logged_in = None):
        self.curr_user = curr_user
        self.logged_in = logged_in 

    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        while(True):
            user = input("What will your twitter handle be?")
            password = input("Enter a password:")
            verify = input(" Re-enter your password:")
            check_new = db_session.query(User).where(User.username == user).all()
            if (verify == password and check_new == None):
                    break
            else:
                print("Those password don't match try again")
        new_user = user(user, password)
        self.logged_in = True
        self.curr_user = new_user
        db_session.add(new_user)
        db_session.commit()
        print("welcome" + user)
            
    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        while(True):
            user = input("Username:")
            password = input("Password:")
            person = db_session.query(User).where(User.password == password and User.username == user).first()
            if(person.username == user and person.password == password):
                break
            else:
                print("Invalid username or password")
        print("Welcome " + person.username + "!")
        self.logged_in = True
        self.curr_user = person
        

    
    def logout(self):
        self.logged_in = False
        self.curr_user = None

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        print("Please select a menu option:")
        option = input("1.Login/n2.Register User/n3.Exit")
        if(option == 1):
            self.login()
        elif(option == 2):
            self.register_user()
        elif(option == 3):
            self.end()

    def follow(self):
        while(True):
            who = input("Who would you like to follow?")
            person = db_session().query(User).where(User.username == who).first()
            if(person in self.curr_user.following):
                print("you are already following this person")
            else:
                break
        follower = Follower(self.curr_user.id, person.id)
        db_session.add(follower)
        db_session.commit()
        print("You are now following " + who)
        
    def unfollow(self):
        while(True):
            who = input("Who would you like to unfollow?")
            person = db_session.query(User).where(User.username == who).first()
            if(person not in self.curr_user.following):
                print("you don't follow this person")
            else:
                break
        db_session.delete(person)
        db_session.commit()
        print("you have unfollowed " + who)


    def tweet(self):
        tweet = input("Create Tweet: ")
        tags = input("Enter your tags seperated by spaces:")
        tag_list = tags.split()
        timestamp = datetime.now()
        new_tweet = Tweet(tweet, timestamp, self.curr_user.username)
        db_session.add(new_tweet)
        db_session.commit()
    
    def view_my_tweets(self):
        result = db_session().query(Tweet).where(self.curr_user.username == Tweet.username).all()
        for tweet in result:
            tweet.__repr__()
            print("===========================")
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        followers = db_session.query(Follower).where(self.curr_user.following).all()
        for follower in followers:
            tweet = db_session.query(Tweet).where(follower.username == Tweet.username).all()
            newest_tweet = tweet(0)
            for tweets in tweet:
                pass
        

    def search_by_user(self):
        pass

    def search_by_tag(self):
        pass

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()
        while(self.logged_in == True):
        
            self.print_menu()
            option = int(input(""))

            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
        
        self.end()
