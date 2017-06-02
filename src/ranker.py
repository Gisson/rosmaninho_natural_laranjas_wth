#!/usr/bin/env python3

class Keys:
    USER = 'user'
    RANKINGS = 'rankings'

class Ranker:
    def __init__(self, user):
        self.user = user
    
    def rank(self):
        return { Keys.USER: self.user,
                 Keys.RANKINGS: { 'critA': 0,
                                  'critB': 0
                                }
               }


