#!/usr/bin/env python3

import re


class Parser:

    def __init__(self, filename):
        self.filename = filename
        self.chapter = 0
        self.paragraph = 0

    def handle_chapter_first(self, line):
        if line.strip() == "I":
            self.chapter = 1
        elif line.strip() == "XXXII":
            self.chapter = 32
        elif line.strip() == "LVI":
            self.chapter = 56
        elif line.strip() == "LXXXV":
            self.chapter = 85
        else:
            raise Exception(line)
        self.paragraph = -1

    def handle_chapter(self, line):
        self.chapter += 1
        self.paragraph = -1

    def handle_para(self, txt):
        self.paragraph += 1
        ref = f"{self.chapter:03d}.{self.paragraph:03d}"
        print(ref, " ".join(txt), sep="\t")

    def parse(self):
        state = 0

        for line in open(self.filename):
            if state == 0:  # frontmatter
                if line.startswith("***"):
                    state = 1
                else:
                    pass  # ignore
            elif state == 1:
                if re.match("[CLXVI]+\n", line):
                    self.handle_chapter_first(line)
                    state = 2
                    txt = []
                else:
                    pass  # ignore
            elif state == 2:
                if line.startswith("***"):
                    if txt:
                        self.handle_para(txt)
                        txt = []
                    state = 3
                elif line.startswith("FIN DU TOME"):
                    if txt:
                        self.handle_para(txt)
                        txt = []
                    state = 3
                elif line == "FIN\n":
                    if txt:
                        self.handle_para(txt)
                        txt = []
                    state = 3
                elif line.strip() == "":
                    if txt:
                        self.handle_para(txt)
                        txt = []
                elif re.match("[CLXVI]+\n", line):  # chapters
                    if txt:
                        self.handle_para(txt)
                        txt = []
                    self.handle_chapter(line)
                # elif re.match("\d+m\n", line):  # page breaks?
                #     if txt:
                #         self.handle_para(txt)
                #         txt = []
                elif line.startswith("FOOTNOTES:"):
                    if txt:
                        self.handle_para(txt)
                        txt = []
                    self.chapter = "FN"
                    self.paragraph = -1
                    self.handle_para([line.strip()])
                else:
                    txt.append(line.strip())
            elif state == 3:  # backmatter
                pass  # ignore
            else:
                raise Exception("unknown state", state)


p = Parser("pg/pg17989.txt")
p.parse()
p = Parser("pg/pg17990.txt")
p.parse()
p = Parser("pg/pg17991.txt")
p.parse()
p = Parser("pg/pg17992.txt")
p.parse()
