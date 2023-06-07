import os
import json
from time import sleep
from database_bot import DataBaseBot
from scraping.web_scraping import WebScraping
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys


# Constants and env variables
load_dotenv ()
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
MESSAGES_PER_DAY = int(os.getenv ("MESSAGES_PER_DAY"))
WAIT_TIME = int(os.getenv ("WAIT_TIME"))

class Bot (WebScraping):
    
    def __init__ (self):
        
        print ("Starting bot...")
        
        # Start chrome
        super().__init__ ()
        
        # Connect to database
        self.db = DataBaseBot ("database_bot.db")

        # Web pages and css selectors
        self.pages = {
            "home": "https://www.instagram.com/",
        }
        self.selectors = {
            "profile_btn": '.xh8yej3.x1iyjqo2 > div:last-child [role="link"]',
            "login_form": '#loginForm',
            "followers": '.x7r02ix.xf1ldfh.x131esax ._aano > div:first-child .xt0psk2 > .xt0psk2 > a',
            "followers_wrapper": '[role="dialog"] ._aano',
            'message_btn': '.x9f619 > [role="button"]',
            "message_textarea": '[role="textbox"]',
            "message_submit": '[tabindex="-1"] [role="button"]:nth-child(3)',
        }        
        
    def auto_run (self):
        """ Run bot automatically """

        # Login and get followrs
        self.__login_cookies__ ()
        followers = self.__get_followers__ ()
        
        # Errors control variables
        self.error = ""
        
        # Save all followers in database, first time
        if self.db.new_database:
            self.__save_initial_followers__ (followers)
        else:
           self.__send_messages__ (followers)
        
        print ("Done")
        
    def __login_cookies__ (self):
        """ Load cookies from local file, to avoid manual login
        """
        
        print ("Loading cookies...")
        
        # Load instagram home page
        self.set_page (self.pages["home"])
        
        # Validate cookies file
        cookies_path = os.path.join (CURRENT_FOLDER, "cookies.json")
        if not os.path.exists (cookies_path):
            print ("Error: Cookies file not found")
            quit ()        
        
        # Get cookies
        with open (cookies_path, "r") as file:
            cookies = json.load (file)
        self.set_cookies (cookies)
        
        # Reload home
        self.set_page (self.pages["home"])
        sleep (5)
        self.refresh_selenium ()
        
        # Validate login
        login_form = self.get_elems (self.selectors["login_form"])
        if login_form:
            print ("Error: Cookies expired")
            quit ()
            
    def __get_followers__ (self) -> list:
        """ Get followers from profile page of the bot

        Returns:
            list: followers profiles
        """
        
        print ("Getting followers...")
        
        # Go to followers page
        self.click_js (self.selectors["profile_btn"])
        followers_page = self.driver.current_url + "followers/"
        self.set_page (followers_page)
        
        more_links = True
        links_found = []
        last_links = []
        while more_links: 
            
            # Get all profile links
            sleep(6)
            self.refresh_selenium()
            links = self.get_attribs(self.selectors["followers"], "href", allow_duplicates=False, allow_empty=False)
            
            # Break where no new links
            if links == last_links: 
                break
            else: 
                last_links = links
            
            # Validate each link
            for link in links: 
                
                # Save current linl
                if link not in links_found: 
                    links_found.append(link)
            
            # Go down
            scroll_elem = self.get_elems (self.selectors["followers_wrapper"])
            if scroll_elem:
                self.driver.execute_script(f"arguments[0].scrollBy (0, {2000});", scroll_elem[0])
        
        return links_found
    
    def __send_message__ (self, user:str, message:list) -> bool:
        """ Send single message to a target user, and update "error" if something goes wrong

        Args:
            user (str): instagram profile link
            message (list): message to send (in lines)
            
        Returns:
            bool: True if message was sent, False otherwise
        """
                
        # Go to target profile
        self.set_page (user)
        sleep (5)
        self.refresh_selenium ()

        # Validate if there is a message button
        message_btn_text = self.get_text (self.selectors["message_btn"])
        if not message_btn_text or message_btn_text.strip().lower() != "message":
            self.error = "error reading profile page: message button not found"
            return False
                
        # Go to message page
        try:
            self.click_js (self.selectors["message_btn"])
            sleep (8)
            self.refresh_selenium ()
        except Exception as e:
            self.error = f"error clicking message button: {e}"
            return False
        
        # Write and submit message
        try:
            self.write_lines (self.selectors["message_textarea"], message)
            self.refresh_selenium ()
            self.click_js (self.selectors["message_submit"])
            sleep (3)
        except Exception as e:
            self.error = f"error sending message: {e}"
            return False
        
        # Return default status
        return True
    
    def __send_messages__ (self, followers:list):
        """ Send messages to followers, validating the maximum number of messages per day

        Args:
            followers (list): followers profiles
        """
        
        # Detect new followers and save in database
        current_followers = self.db.get_current_followers ()
        new_followers = list(filter(lambda follower: follower not in current_followers, followers))
        
        # Detect and save new followers
        if new_followers:
            print (f"{len(new_followers)} new followers detected:")
            for follower in new_followers:
                print (follower)
                self.db.add_message (follower)
        else:                    
            print ("No new followers detected")
            
        # Count messages
        print (f"\nMessages per day: {MESSAGES_PER_DAY}")
        
        messages_sent_today = self.db.count_messages_sent_today ()
        print (f"Messages sent today: {messages_sent_today}")            
        
        messages_to_send_num = MESSAGES_PER_DAY - messages_sent_today
        if messages_to_send_num <= 0:
            print ("No more messages to sent today")
            quit ()            
            
        print (f"Sending {messages_to_send_num} messages...")
        print ("\tMessage (type 'quit' to end):")
        message_text = []
        while True:
            user_input = input ()
            if user_input.lower().strip() == "quit":
                break
            message_text.append (user_input)
        
        # send message to follower
        messages_to_send =self.db.get_messages_to_send ()
        for message in messages_to_send[:messages_to_send_num]:
            
            user = message[0]
                            
            # submit message
            print (f"Sending message to {user}...")
            message_sent = self.__send_message__ (user, message_text)
            
            # Show and update database
            if message_sent:
                self.db.update_message (user, message_text, sent=1)
                print ("\tMessage sent")
            else:
                self.db.update_message (user, f" {self.error}", sent=3)
                print (f"\t{self.error}")
            
            # Wait
            print (f"Waiting {WAIT_TIME} minutes...")
            sleep (WAIT_TIME * 60)
    
    
    def __save_initial_followers__ (self, followers:list):
        """ Save initial followers in database with sent=2

        Args:
            followers (list): profiles of followers
        """
        
        print ("Saving initial followers in database...")
        
        for follower in followers:
            self.db.add_message (follower, sent=2)
            
                
if __name__ == "__main__":
    # Test bot
    bot = Bot ()
    bot.auto_run ()