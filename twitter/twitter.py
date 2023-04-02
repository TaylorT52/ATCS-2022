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
        pass

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
            print("You are now following " + follow)

        self.run()

    def unfollow(self):
        pass

    def tweet(self):
        pass
    
    def view_my_tweets(self):
        pass
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
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
        if(self.logged_in == None):
            init_db()

            print("Welcome to ATCS Twitter!")
            self.startup()

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
