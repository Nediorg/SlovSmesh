from dotenv import load_dotenv
from os import environ
import os.path

load_dotenv()

DEFAULT_WORDLIST_PATH = os.path.join(os.path.dirname(__file__), '../data/wordlist.txt')
DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), '../data/db.sqlite3')

class Config(object):
    WORDLIST_PATH = environ.get('WORDLIST_PATH', DEFAULT_WORDLIST_PATH)
    DB_PATH = environ.get('DB_PATH', DEFAULT_DB_PATH)
