from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
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
        repeat = False
        existing_users = db_session.query(User.username).all()
        while not repeat:
            name = input("What will your Twitter handle be? ")
            if name in existing_users:
                repeat = True
                break
            pswd = input("Enter a password: ")
            retry = input("Reenter your password: ")
            repeat = pswd == retry

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        pass

    
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
        pass

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
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()

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
