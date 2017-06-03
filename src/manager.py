#!/usr/bin/env python3

from github import Github
import os
import logging

# swinging the code hammer ^_^'
log_level = logging.INFO
logging.basicConfig(level = log_level)
logger = logging.getLogger(__name__)
logger.level = log_level


class Keys:
    USER = 'user'
    RANKINGS ='rankings'

class Manager:
    @staticmethod
    def getGithub():
        logger.info("[MANAGER] - Instantiating the Github object")
        return Github(os.environ.get("GITHUB_API_TOKEN"))
    
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

