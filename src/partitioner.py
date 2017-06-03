#!/usr/bin/env python3

from block import *
import base64
import re
import logging
from manager import Manager
from block import *

log_level = logging.INFO
logging.basicConfig(level = log_level)
logger = logging.getLogger(__name__)
logger.level = log_level

class Partitioner:
    def __init__(self, author, files):
        logger.info("[PARTITIONER] - Initializing")
        self.files = files
        self.author = author

    def get_code_elements(self):
        for fil in self.files:
            print(fil.patch)
        return [CodeElement()]
regex="@@ -(\d+),(\d+) \+(\d+),(\d+) @@"
ignoreregex="-(.*)"
class DiffParser:
    def __init__(self,author):
        self.blocks=[]
        self.author=author

    def parse(self,diff):
        wantedStuff=[]
        difftuple=diff.split("\n")[4:]
        for line in difftuple:
            match=re.match(r""+regex,line)
            nomatch=re.match(r""+ignoreregex,line)
            if nomatch:
                continue
            elif match:
                print("Making block")
                if not wantedStuff:
                    continue
                self.blocks+=[Block(wantedStuff)]
                wantedStuff=[]
            elif not match and not nomatch:
                wantedStuff+=[Line(self.author,0,line)]
                print("It matched")
            else:
                print("Da fak?")
        self.blocks+=[Block(wantedStuff)]
        return self.blocks
        #self.old_start_line=match.group(1)
        #self.old_line_size=match.group(2)
        #self.new_start_line=match.group(3)
        #self.new_line_size=match.group(4)
