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

class UserAttributes:
    AVATAR_URL="avatarurl"
    BIO="bio"
    CONTRIBUTIONS="contrib"
    EMAIL="email"
    HIREABLE="hireable"
    NAME="name"

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
        self.user_bio=userobj.bio if userobj.bio else ""
        self.user_contributions=userobj.contributions if userobj.contributions else ""
        self.user_email=userobj.email if userobj.email else ""
        self.user_hireable=userobj.hireable if userobj.hireable else ""
        self.user_name=userobj.name
        self.repositories = Repos(user)
        self.ranker = Ranker(user)
        self.filename_filter=".*"

    def set_filename_filter(self, pattern):
        """ filter the files in the repo using a pattern in the filename"""
        self.filename_filter = pattern
        return self

    def add_tech(self, techname):
        """filter user repos by technology"""
        self.repositories.add_tech(techname)
        return self

    def add_filter(self, weight, pattern):
        self.ranker.add_filter(int(weight), pattern)
        print("add filter: " + pattern)
        return self

    def rank(self):
        ranks = {'rank': 0, 'matches': {}, 'weak-matches': {},'repos-with': {'wiki-enabled': 0, 'wiki-disabled': 0}}
        results = self.repositories.get_repos()
        logger.info("ranking " + str(len(results)) + " repos")
        for repo in results:
            logger.debug("rank_repo_name: " + repo.name)
            commits = repo.get_commits(author=self.user)
            if commits:
                repos_with = ranks['repos-with']
                if repo.has_wiki:
                    repos_with['wiki-enabled']+=1
                else:
                    repos_with['wiki-disabled']+=1
            else:
                logger.info("no commits in repo " + repo.name)
                continue
            blocks = []
            for c in commits:
                logger.debug("commit_sha: "+c.sha)
                # filter filenames
                for f in list(c.files):
                    if not re.search(self.filename_filter, f.filename):
                        logger.info("Ignoring File: "+f.filename)
                        c.files.remove(f)

                if c.files == [] or c.files == None:
                    logger.info("no files in commit "+c.sha+" in repo " + repo.name)
                    continue
                part = Partitioner(self.user, c.files)
                blocks += part.get_code_elements()
            b = Block(blocks)

            matches = b.accept(self.ranker)
            matches.pop(Keys.USER, None)
            ranks = sum_dict(ranks, matches)
        ranks[Keys.USER] = self.user
        return ranks
    def get_user_info(self):
    #        logger.debug({UserAttributes.AVATAR_URL : self.user_avatarurl,UserAttributes.BIO : self.user_bio, UserAttributes.CONTRIBUTIONS : self.user_contributions, UserAttributes.EMAIL : self.user_email, UserAttributes.HIREABLE : self.user_hireable, UserAttributes.NAME : self.user_name})
        return {UserAttributes.AVATAR_URL : self.user_avatarurl,UserAttributes.BIO : self.user_bio, UserAttributes.CONTRIBUTIONS : self.user_contributions, UserAttributes.EMAIL : self.user_email, UserAttributes.HIREABLE : self.user_hireable, UserAttributes.NAME : self.user_name}

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

def test2():
    man = Manager("nuno-silva")
    man.add_tech("C")
    #man.set_filename_filter(".*\.[c|h]")
    man.add_filter(2, "struct")
    man.add_filter(-1, "\*")
    return man.rank()
