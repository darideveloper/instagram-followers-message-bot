from database_bot import DataBaseBot

class Bot ():
    
    def __init__ (self):
        
        # Connect to database
        self.db = DataBaseBot ("database_bot.db")
        input ("end?")
        
if __name__ == "__main__":
    # Test bot
    Bot ()