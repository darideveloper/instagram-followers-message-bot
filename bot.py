import os
import json
from time import sleep
from database_bot import DataBaseBot
from scraping.web_scraping import WebScraping

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

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
        }        

        # Login and get followrs
        self.__login_cookies__ ()
        followers = self.__get_followers__ ()
        
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
        
        
        
        
        
 
        
        
        
if __name__ == "__main__":
    # Test bot
    Bot ()