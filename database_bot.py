from database.sqlite import DataBase
from datetime import datetime

class DataBaseBot (DataBase):
    
    def __create_database__(self):
        self.run_sql ("CREATE TABLE IF NOT EXISTS messages (user char, date char, message char DEFAULT '', sent int DEFAULT 0, PRIMARY KEY (user, date))")
    
    def get_messages (self)  -> list:
        """ Get all messages from database

        Returns:
            list: messages data (user, date, message, sent)
        """
        
        # Get roes from database
        messages = self.run_sql ("SELECT * FROM messages")
        
        # Format dates from iso
        if messages:
            messages = list(map(lambda row: (row[0], self.get_date_from_iso(row[1]), row[2], row[3]), messages))
                
            return messages
        else:
            return []
    
    def count_messages_sent_today (self) -> int:
        """ Get number of messages sent today

        Returns:
            int: number of messages
        """
        
        current_messages = self.get_messages ()
        messages_sent = list(filter(lambda message: message[3] == 1, current_messages))
        messages_sent_today = list(filter(lambda message: message[1].date() == datetime.now().date(), messages_sent))
        
        return len (messages_sent_today)
    
    def get_messages_to_send (self) -> list:
        """ Get messages to send

        Returns:
            list: messages data (user, date, message, sent)
        """
        
        current_messages = self.get_messages ()
        messages_to_send = list(filter(lambda message: message[3] == 0, current_messages))
        
        return messages_to_send
    
    def get_current_followers (self) -> list:
        """ Get profile links / followers in database 

        Returns:
            list: profile links
        """
        current_messages = self.get_messages ()
        current_followers = list(map(lambda message: message[0], current_messages))
        
        return current_followers
        
    
    def delete_messages (self):
        """ Delete all messages from database
        """
        self.run_sql ("DELETE FROM messages")
        
    def add_message (self, user:str, message:str="", date:datetime=None, sent:int=0):
        """ Add message to database

        Args:
            user (str): instagram profile link of user
            message (str): message sent by bot
            date (datetime, optional): date where the message was sent, or date of new follower detection. Defaults to None.
        """
        
        # Convert date to iso or get today date
        if date:
            date_iso = self.get_date_iso (date)
        else:
            date_iso = self.get_now_iso ()
            
        
        self.run_sql (f"INSERT INTO messages (user, date, message, sent) VALUES ('{user}', '{date_iso}', '{message}', {sent})")
        
    def update_message (self, user:str, message:str="", date:datetime=None, sent:int=0):
        """ Update message in database

        Args:
            user (str): instagram profile link of user
            message (str): message sent by bot
            date (datetime, optional): date where the message was sent, or date of new follower detection. Defaults to None.
        """
        
        if type(message) == list:
            message = "\n".join(message)
        
        # Convert date to iso or get today date
        if date:
            date_iso = self.get_date_iso (date)
        else:
            date_iso = self.get_now_iso ()
        
        self.run_sql (f"UPDATE messages SET message='{message}', date='{date_iso}', sent={sent} WHERE user='{user}'")