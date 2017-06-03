#!/usr/bin/env python3

import re
import logging
from collections import defaultdict

from block import *
from repos import *

logger = logging.getLogger(__name__)

class Keys:
    USER = 'user'
    MATCHES = 'matches'
    WEAK_MATCHES = 'weak-matches'
    RANK = 'rank'

class Filter:
    def __init__(self, weight, pattern):
        self.weight = weight
        self.pattern = pattern

class Ranker:
    def __init__(self, user):
        self.user = user
        self.filters = [] # list of {'weight': ..., 'pattern': ...}

    def add_filter(self, weight, pattern):
        self.filters += [Filter(weight, pattern)]
        return self
    """
    1. when a match is found on a line that the user didn't author, we
       count that as a weak-match: since the user changed the block,
       he had to know what that piece of code did, so the weight of the match is 1/linecount.
    """
    def visit_block(self, block):
        ret = {Keys.USER: self.user, Keys.RANK: 0, Keys.MATCHES: {}, Keys.WEAK_MATCHES: {}}
        for elm in block.code_elements:
            if isinstance(elm, Line):
                if elm.author == self.user:
                    matches = self.visit_line(elm)
                    ret[Keys.RANK] += matches[Keys.RANK]
                    ret[Keys.MATCHES] = sum_dict(ret[Keys.MATCHES], matches[Keys.MATCHES])
                    ret[Keys.WEAK_MATCHES] = sum_dict(ret[Keys.WEAK_MATCHES], matches[Keys.WEAK_MATCHES])
                else:
                    matches = self.visit_line(elm, False)
                    ret[Keys.RANK] += 1/block.linecount * matches[Keys.RANK]
                    ret[Keys.WEAK_MATCHES] = sum_dict(ret[Keys.WEAK_MATCHES], matches[Keys.MATCHES])
            elif isinstance(elm, Block):
                matches = elm.accept(self)
                ret[Keys.RANK] += matches[Keys.RANK]
                ret[Keys.MATCHES] = sum_dict(ret[Keys.MATCHES], matches[Keys.MATCHES])
                ret[Keys.WEAK_MATCHES] = sum_dict(ret[Keys.WEAK_MATCHES], matches[Keys.WEAK_MATCHES])
            else:
                logger.erro("unknown code_element type")
        return ret

    """ returns a list of matches for the given line
        e.g. {'user': 'nuno-silva', 'rank': -1, 'matches': {'Thread': 2, 'new': 1}, 'weak-matches': {'Thread': 2, 'new': 1}}
    """
    def visit_line(self, line, check_author=True):
        logger.debug('visit_line: ' +  str(line.lineno))
        if check_author and line.author != self.user:
            return {Keys.USER: self.user, Keys.RANK: 0, Keys.MATCHES: {}, Keys.WEAK_MATCHES: {}}
        rank = 0
        match_counts = {}
        for filter in self.filters:
            matches = re.findall(filter.pattern, line.code)
            if matches:
                for match in matches:
                    match_counts[filter.pattern] = match_counts[filter.pattern]+1 if (filter.pattern in match_counts) else 1
                    logger.debug("Ranker: '" + filter.pattern + "' match on line " + str(line.lineno) + ': ' + match)
                    rank += filter.weight
        return {Keys.USER: line.author, Keys.RANK: rank, Keys.MATCHES: match_counts, Keys.WEAK_MATCHES: {}}

def test_ranker():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG

    elm = Line("nuno-silva", 1, "Thread t = new Thread();")
    r = Ranker("nuno-silva")
    print("0", elm.accept(r))
    r.add_filter(2, "Thread")
    r.add_filter(-5, "new")
    print("-1", elm.accept(r))
    b = Block()
    b.add_code_element(elm)
    b.add_code_element(Line("gisson", 2, "t = new Thread();"))
    print("-2.5", b.accept(r))
    b2 = Block()
    b2.add_code_element(b)
    b2.add_code_element(Line("rato", 3, "t = new Thread();"))
    print("-3.5", b2.accept(r))

def sum_dict(a, b):
    "recursively sums the values of a with the values of b"
    a = dict(a)
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                a[key] = sum_dict(a[key], b[key])
            else:
                a[key] += b[key]
        else: # merge
            if isinstance(b[key], dict):
                a[key] = dict(b[key])
            else:
                a[key] = b[key]
    return a
