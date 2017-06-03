#!/usr/bin/env python3

import re
import logging
from collections import defaultdict

from block import *

logger = logging.getLogger(__name__)
    
class Keys:
    USER = 'user'
    MATCHES = 'matches'
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

    def visit_block(self, block):
        logger.error('not implemented')
        pass

    """ returns a list of matches for the given line
        e.g. {'user': 'nuno-silva', 'rank': -1, 'matches': {'Thread': 2, 'new': 1}}
    """
    def visit_line(self, line):
        logger.debug('visit_line: ' +  str(line.lineno))
        if line.author != self.user:
            return {Keys.USER: self.user, Keys.RANK: 0, Keys.MATCHES: {}}
        rank = 0
        match_counts = {}
        for filter in self.filters:
            matches = re.findall(filter.pattern, line.code)
            if matches:
                for match in matches:
                    match_counts[filter.pattern] = match_counts[filter.pattern]+1 if (filter.pattern in match_counts) else 1
                    logger.debug("Ranker: '" + filter.pattern + "' match on line " + str(line.lineno) + ': ' + match)
                    rank += filter.weight
        return {Keys.USER: self.user, Keys.RANK: rank, Keys.MATCHES: match_counts}

def test():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG

    elm = Line("nuno-silva", 1, "Thread t = new Thread();")
    r = Ranker("nuno-silva")
    print("0", elm.accept(r))
    r.add_filter(2, "Thread")
    r.add_filter(-5, "new")
    print("-1", elm.accept(r))
