# Imports
import datetime

class Settings(object):
    def __init__(self, settings_dict):
        self.name = settings_dict['name']
        self.screen_name = settings_dict['screen_name']
        self.owner = settings_dict['owner']

        self.announce = settings_dict['messages']['announce']
        self.shutdown = settings_dict['messages']['shutdown']

        self.twitter = settings_dict['twitter']

    # Replaces %TIME% with the current timestamp
    def parse_message(self, message):
        res = message.replace('%TIME%', datetime.datetime.now().strftime('%H:%M:%S'))
        return res

    # Get methods that will parse the messages (Include timestamp)
    def get_announce(self):
        return self.parse_message(self.announce)

    def get_shutdown(self):
        return self.parse_message(self.shutdown)