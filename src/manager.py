#!/usr/bin/env python3

from github import Github
import os
import logging

from repos import *
from  partitioner import Partitioner
from block import *
from ranker import *

# swinging the code hammer ^_^'
log_level = logging.DEBUG
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
        userobj=Manager.getGithub().get_user(login=user)
        self.user_avatarurl=userobj.avatar_url
        self.user_bio=userobj.bio
        self.user_contributions=userobj.contributions
        self.user_email=userobj.email
        self.user_hireable=userobj.hireable
        self.user_name=userobj.name
        self.repositories = Repos(user)
        self.ranker = Ranker(user)
        
   

    def add_tech(self, techname):
        """filter user repos by technology"""
        self.repositories.add_tech(techname)
        return self

    def add_filter(self, weight, pattern):
        self.ranker.add_filter(int(weight), pattern)
        return self

    def rank(self):
        ranks = {}
        results = self.repositories.get_repos()
        for repo in results:
            logger.debug("rank_repo_name: " + repo.name)
            commits = repo.get_commits(author=self.user)
            blocks = []
            for c in commits:
                logger.debug("commit_sha: "+c.sha)
                part = Partitioner(self.user, c.files)
                blocks += part.get_code_elements()
            b = Block(blocks)
            
            matches = b.accept(self.ranker)
            matches.pop(Keys.USER, None)
            ranks = sum_dict(ranks, matches)
        ranks[Keys.USER] = self.user
        return ranks

def test():
    repo = testr()[0]
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
