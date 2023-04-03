from models import *
from database import init_db, db_session
from datetime import datetime
import itertools

class Twitter:
    logged_in = None

    """
    The menu to print once a user has logged in
    """
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
        user_repeat = True
        valid_password = False
        existing_users = list(itertools.chain(*db_session.query(User.username).all()))
        
        while user_repeat:
            name = input("What will your Twitter handle be? ")
            user_repeat = name in existing_users
            if user_repeat:
                print("That user already exists. Try again. \n")
            
        while not valid_password:
            pswd = input("Enter a password: ")
            retry = input("Reenter your password: ")
            valid_password = pswd == retry
            if not valid_password:
                print("That password is invalid. Try again \n")

        new_user = User(username=name, password=pswd)
        db_session.add(new_user)
        db_session.commit()
        self.logged_in = new_user

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        invalid = True
        existing_users = db_session.query(User.username, User.password).all()
        while invalid:
            username = input("Input your username: ")
            password = input("Input your password: ")
            invalid = not (username, password) in existing_users
            if invalid: 
                print("Invalid username or password. Try again. \n")

        self.logged_in = db_session.query(User).where(User.username == username).first()
        print("Success!")

    def logout(self):
        self.logged_in = None

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        choose = int(input("Please select a menu option \n 0. Login \n 1. Register User \n 2. Exit \n"))
        if choose == 0:
            self.login()
        elif choose == 1:
            self.register_user()
        elif choose == 2:
            self.end()
        else:
            print("Sorry, your input was invalid")

    #Follow users
    def follow(self):
        username = input("Who would you like to follow? ")
        follow = db_session.query(User).where(User.username == username).first()
        if follow == None:
            print("This user does not exist! Try again. \n")
        elif follow in self.logged_in.following:
            print("You already follow " + str(follow) + "! Try again. \n")
        else: 
            following = Follower(follower_id = self.logged_in.username, following_id = follow.username)
            db_session.add(following)
            db_session.commit()
            print("You are now following " + str(follow))

    #Unfollow users 
    def unfollow(self):
        user = input("Who would you like to unfollow? ")
        user = db_session.query(User).where(User.username == user).first()
        
        if user == None:
            print("This user does not exist. Try again.")
        elif user not in self.logged_in.following:
            print("You don't follow " + str(user))
        else:
        #Previously got 3 on using SQL to insert, update, and delete data because data wasn't deleted on quiz - here is example :)
            to_del = db_session.query(Follower).where((Follower.following_id == user.username) & (Follower.follower_id == self.logged_in.username)).first()
            db_session.delete(to_del)
            db_session.commit()
            print("You have now unfollowed " + str(user))

    #creates tweet, tags, and then connects tweets and tags
    def tweet(self):
        tweet_content = input("Create Tweet: ")
        tags = input("Add tags: ")
        tags = list(filter(lambda x: not x == "", tags.split("#")))
        timestamp = str(datetime.now())
        tweet = Tweet(content = tweet_content, timestamp = timestamp, username = self.logged_in.username)
        db_session.add(tweet)
        db_session.flush()

        for tag_content in tags:
            existing = db_session.query(Tag).where(tag_content == Tag.content).first()
            if existing == None:
                add = Tag(content = tag_content)
                db_session.add(add)
                existing = add
            rel = TweetTag(tweet_id = tweet.id, tag_id = existing.id)
            db_session.add(rel)
            db_session.flush()

        db_session.commit()
    
    #See all personal tweets
    def view_my_tweets(self):
        tweets = db_session.query(Tweet).where(Tweet.username == self.logged_in.username).all()
        self.print_tweets(tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    by getting all tweets and checking which are from ppl user follows, then get last 5 (so most recent)
    """
    def view_feed(self):
        valid_tweets = db_session.query(Tweet).all()
        following = list(map(lambda x: x.username, self.logged_in.following))
        valid_tweets = list(filter(lambda x: x.username in following, valid_tweets))[-5:]
        self.print_tweets(valid_tweets)

    #Searches for tweet by user
    def search_by_user(self):
        user = input("What user's tweets would you like to see? ")
        if not user in list(itertools.chain(*db_session.query(User.username).all())):
            print("This user does not exist.")
        else:
            tweets = db_session.query(Tweet).where(Tweet.username == user)
            self.print_tweets(tweets)

    #Searches for tweets by tag by finding tag, getting tweets then filtering
    def search_by_tag(self):
        test_tag = input("What tag would you like to search for? ").replace("#", "")
        test_tag = db_session.query(Tag).where(Tag.content == test_tag).first()
        tweets = db_session.query(Tweet).all()
        tweets = list(filter(lambda x: test_tag in x.tags, tweets))
        self.print_tweets(tweets)

        if len(tweets) == 0:
            print("No tweets exist with this tag!")
   
    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()

        while not self.logged_in == None:
            self.print_menu()
            option = int(input("Choose an option: "))

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
