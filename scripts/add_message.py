# add manually a register of a new message

# Add parent path
import os
import sys
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(CURRENT_FOLDER)
sys.path.append(PARENT_FOLDER)

# Import database
from database_bot import DataBaseBot

DataBaseBot ("database_bot.db").add_message ("sample user", "sample message")

print ("done")