#!/usr/bin/env python3

from github import Github
import os
import logging

import repos
from  partitioner import Partitioner
from block import *
from ranker import *

# swinging the code hammer ^_^'
log_level = logging.INFO
logging.basicConfig(level = log_level)
logger = logging.getLogger(__name__)
logger.level = log_level


class Keys:
    USER = 'user'
    RANKINGS ='rankings'

class Limits:
    MAX_FILES = 30
    MAX_REPOS = 5

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

def test():
    repo = repos.test()[0]
    commits = repo.get_commits(author="nuno-silva")
    blocks = []
    for c in commits:
        part = Partitioner("nuno-silva", c.files)
        blocks += part.get_code_elements()
    b = Block(blocks)
    
    r = Ranker("nuno-silva")
    r.add_filter(2, "private")
    r.add_filter(0.1, "public")
    r.add_filter(-5, "static")
    return b.accept(r)
