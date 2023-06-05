# show all messages in database

# Add parent path
import os
import sys
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(CURRENT_FOLDER)
sys.path.append(PARENT_FOLDER)

# Import database
from database_bot import DataBaseBot

db = DataBaseBot ("database_bot.db")
messages = db.get_messages ()

print ("Sent values:")
print ("0. Message ready to send")
print ("1. Message sent")
print ("2. Initial follower")

print ("\nuser, date, message, sent")

for message in messages:
    print (message)
    
print ("done")