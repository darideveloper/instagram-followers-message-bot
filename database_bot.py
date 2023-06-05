from database.sqlite import DataBase
from datetime import datetime

class DataBaseBot (DataBase):
    
    def __create_database__(self):
        self.run_sql ("CREATE TABLE IF NOT EXISTS messages (user char, date char, message char DEFAULT '', sent int DEFAULT 0, PRIMARY KEY (user, date))")
    
    def get_messages (self):
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