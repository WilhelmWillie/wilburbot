# Imports
from wilbur import Wilbur
from settings import Settings
import paths
import yaml
import sys

'''
Check for arguments
--announce = Tweet an announcement tweet when Wilbur is started
--debug    = Local debugging using CLI
'''
ANNOUNCE = "--announce" in sys.argv or "--a" in sys.argv
DEBUG = "--debug" in sys.argv or "--d" in sys.argv

# Load in settings and convert to settings object
SETTINGS_DICT = yaml.safe_load(file(paths.SETTINGS_PATH, 'r'))
SETTINGS = Settings(SETTINGS_DICT)

# Run Wilbur
if __name__ == '__main__':
    wilbur = Wilbur(settings=SETTINGS, debug=DEBUG, announce=ANNOUNCE)
    wilbur.run()