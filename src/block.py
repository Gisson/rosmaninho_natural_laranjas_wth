#!/usr/bin/env python

class CodeElement:
    def accept(self, ranker):
        pass

class Line(CodeElement):
    def __init__(self, author, lineno, code):
        # TODO
        pass

    def accept(self, ranker):
        return ranker.visit_line(self)

class Block(CodeElement):
    def __init__(self):
        self.code_elements = []

    def add_code_element(self, code_element):
        self.code_elements += [code_element]

    def add_code_elements(self, code_elements):
        self.code_elements += code_elements

    def accept(self, ranker):
        return ranker.visit_block(self)

