#!/usr/bin/env python3

class Keys:
    USER = 'user'
    RANKINGS = 'rankings'

class Ranker:
    def __init__(self):
        self.user = user

    def add_filter(self, weight, pattern):
        # TODO
        return
    
    def visit(self, code_element):
        # TODO
        return { Keys.USER: self.user,
                 Keys.RANKINGS: { 'critA': 0,
                                  'critB': 0
                                }
               }


