#!/usr/bin/env python


# composite pattern
class CodeElement:
    def accept(self, ranker):
        pass

class Line(CodeElement):
    def __init__(self, author, lineno, code):
        self.author = author
        self.lineno = lineno
        self.code = code
        self.linecount = 1

    def accept(self, ranker):
        return ranker.visit_line(self)

class Block(CodeElement):
    def __init__(self,code_elements=[]):
        self.code_elements = code_elements
        self.linecount = 0
        for elm in code_elements:
            self.linecount += elm.linecount

    def add_code_element(self, code_element):
        self.code_elements += [code_element]
        self.linecount += code_element.linecount
        return self

    def add_code_elements(self, code_elements):
        self.code_elements += code_elements
        for elm in code_elements:
            self.linecount += elm.linecount
        return self

    def accept(self, ranker):
        return ranker.visit_block(self)

