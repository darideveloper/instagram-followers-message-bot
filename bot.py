import os
import json
from database_bot import DataBaseBot
from scraping.web_scraping import WebScraping

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

class Bot (WebScraping):
    
    def __init__ (self):
        
        print ("Starting bot...")
        
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
        }        

        # Workflow    
        self.__login_cookies__ ()
        
        print ()
        
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
        
        # Validate login
        login_form = self.get_elems (self.selectors["login_form"])
        if login_form:
            print ("Error: Cookies expired")
            quit ()
        
 
        
        
        
if __name__ == "__main__":
    # Test bot
    Bot ()