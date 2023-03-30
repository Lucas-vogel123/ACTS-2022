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
            verify = input("Re-enter your password:")
            check_new = db_session.query(User).where(User.username == user).all()
            if(verify == password):
                break
            else:
                print("Those password don't match try again")
        new_user = User(user, password)
        self.logged_in = True
        self.curr_user = new_user
        db_session.add(new_user)
        db_session.commit()
        print("welcome " + user)
            
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
        option = input("1.Login\n2.Register User\n3.Exit")
        if(option == "1"):
            self.login()
        elif(option == "2"):
            self.register_user()
        elif(option == "3"):
            self.end()

    def follow(self):
        who = input("Who would you like to follow?")
        person = db_session().query(User).where(User.username == who).first()
        if(person == None):
            print("This person doesn't exist")
            return
        if(person.username in self.curr_user.following):
            print("you are already following this person")
            return
        self.curr_user.following.add(person)
        db_session.commit()
        print("You are now following @" + who)
        
    def unfollow(self):
        who = input("Who would you like to unfollow?")
        person = db_session().query(User).where(User.username == who).first()
        if(person == None):
            print("This person doesn't exist")
            return
        if(person.username not in self.curr_user.following):
            print("you don't follow this person")
            return
        self.curr_user.following.remove(person)
        db_session.commit()
        print("You have unfollowed @" + who)
       
    def tweet(self):
        tweet = input("Create Tweet: ")
        tags = input("Enter your tags seperated by spaces:")
        tag_list = tags.split()
        timestamp = datetime.now()
        new_tweet = Tweet(tweet, timestamp, self.curr_user.username)
        db_session.add(new_tweet)
        db_session.commit()
        print(new_tweet)
    
    def view_my_tweets(self):
        result = db_session().query(Tweet).where(self.curr_user.username == Tweet.username).all()
        for tweet in result:
            print(tweet)
            print("===========================")
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        # join tweets with followers on follower_id and tweets username where curr_user.username = following_id
        tweets = db_session.query(Tweet).join(Follower, Tweet.username == Follower.follower_id).where(self.curr_user.username == Follower.following_id).order_by(Tweet.timestamp.desc()).limit(5)
        for tweet in tweets:
            print(tweet)
                
    def search_by_user(self):
        username = input("search for user:")
        user = db_session.query(User).where(User.username == username).first()
        if(user == None):
            print("There is no user by that name")
            return
        tweets = db_session.query(Tweet).where(user.username == Tweet.username)
        for tweet in tweets:
            print(tweet)

    def search_by_tag(self):
        tag_input = input("search for tag:")
        tag = db_session.query(Tag).where(tag_input.content == Tag.content).all()
        if(tag == None):
            print("There is no tag with that content.")
            return
        tweets = db_session.query(Tweet).where(Tweet.tags == )
        for tweet in tweets:
            print(tweet)
        

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
