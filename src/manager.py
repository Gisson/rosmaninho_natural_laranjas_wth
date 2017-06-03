#!/usr/bin/env python3
import os

class Keys:
    USER = 'user'
    RANKINGS ='rankings'

class Manager:
    def __init__(self, user):
        self.user = user
    
    def add_tech(self, techname):
        # TODO
        pass

    def add_filter(self, filter_type, value):
        # TODO
        pass

    def rank(self):
        return { Keys.USER: self.user,
                Keys.RANKINGS: { 'critA': 0,
                                  'critB': 0
                                }
               }

def getApiToken():
    return os.environ['GITHUB_API_TOKEN']
