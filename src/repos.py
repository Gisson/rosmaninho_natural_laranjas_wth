#!/usr/bin/env python3

from github import Github
from manager import *
import os
import logging

logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)
logger.level = logging.INFO 

class Repos:
    def __init__(self, user):
        logger.info("[REPOS] - Initializing")
        self.user = user
        self.techs = []
        logger.info("[REPOS] - Instantiating the Github object")
        self.github = Manager.getGithub()
        logger.info("[REPOS] - Intialized!")

    def add_tech(self, tech):
        logger.info("[REPOS] - Adding tech filter \"" + tech + "\"")
        self.techs += [tech]

    """
        Returns a list of github.Repository.Repository objects
        where all of the techs in self.techs can be found.
    """
    def get_repos(self):
        logger.info("[REPOS] - Starting the search for user " + self.user + "'s repos")
        filtered_repos = []
        logger.info("[REPOS] - Getting their repos")
        repos = self.github.get_user(self.user).get_repos()

        for repo in repos:
            logger.info("[REPOS] - Checking their repos against the techs=" + str(self.techs))
            if all(lang in repo.get_languages() for lang in self.techs):
                filtered_repos += [repo]
                logger.info("[REPOS] - " + repo.name + " matched!")
            else:
                logger.info("[REPOS] - " + repo.name + " did not match")

        logger.info("[REPOS] - Returning the matching list of repos=" + str(filtered_repos))
        return filtered_repos

if(logger.level == logging.DEBUG):
    # Just to test this one class
    r = Repos("rodrigorato")
    r.add_tech("Java")
    for repo in r.get_repos():
        print(repo.name)
