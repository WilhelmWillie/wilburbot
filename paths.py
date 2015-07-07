# Imports
import os
import sys

#File paths for Wilbur, commands folder, and settings YAML file
WILBUR_PATH = os.path.dirname(os.path.realpath(sys.argv[0])) # Directory containing WilburBot scripts
CMD_PATH = os.path.join(WILBUR_PATH, "commands")             # Directory where commands are stored
SETTINGS_PATH = os.path.join(WILBUR_PATH, "settings.yml")    # Path for the settings YAML file
STATIC_PATH = os.path.join(WILBUR_PATH, "static")            # Directory where static files used by commands are stored

def static_file(fname):
    return os.path.join(STATIC_PATH, fname) # Returns the absolute path for any static file