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
        fileblocks=[]
        for fil in self.files:
            fileblocks+=DiffParser.parse(self.author,fil.patch)
        return fileblocks
regex="@@ -(\d+),(\d+) \+(\d+),(\d+) @@"
ignoreregex="-(.*)"
class DiffParser:

    @staticmethod
    def parse(author,diff):
        blocks=[]
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
                blocks+=[Block(wantedStuff)]
                wantedStuff=[]
            elif not match and not nomatch:
                wantedStuff+=[Line(author,0,line)]
                print("It matched")
            else:
                print("Da fak?")
        blocks+=[Block(wantedStuff)]
        return blocks
        #self.old_start_line=match.group(1)
        #self.old_line_size=match.group(2)
        #self.new_start_line=match.group(3)
        #self.new_line_size=match.group(4)
