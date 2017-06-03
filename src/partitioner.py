#!/usr/bin/env python3

from block import *
import base64
import re
import logging
from manager import *
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
mylineregex="\+(.*)"
class DiffParser:

    @staticmethod
    def parse(author,diff):
        blocks=[]
        wantedStuff=[]
        difftuple=diff.split("\n")[4:]
        for line in difftuple:
            diffsectionstart=re.match(r""+regex,line)
            nomatch=re.match(r""+ignoreregex,line)
            myline=re.match(r""+mylineregex,line)
            if nomatch:
                continue
            elif diffsectionstart:
                print("Making block")
                if not wantedStuff:
                    continue
                blocks+=[Block(wantedStuff)]
                wantedStuff=[]
            elif not diffsectionstart and not nomatch:
                if myline:
                    wantedStuff+=[Line(author,0,myline.group(1))]
                else:
                    wantedStuff+=[Line("",0,line)]
                logger.info("It matched")
            else:
                logger.info("Da fak?")
        blocks+=[Block(wantedStuff)]
        return blocks
        #self.old_start_line=match.group(1)
        #self.old_line_size=match.group(2)
        #self.new_start_line=match.group(3)
        #self.new_line_size=match.group(4)
