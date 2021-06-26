#!/usr/bin/env python3

import re


class Parser:

    def __init__(self, filename):
        self.filename = filename
        self.volume = 0
        self.chapter = 0
        self.paragraph = 0

    def handle_volume(self, line):
        self.volume += 1

    def handle_chapter(self, line):
        self.chapter += 1
        self.paragraph = 0
        if isinstance(self.chapter, int):
            ref = f"{self.volume}.{self.chapter:03d}.{self.paragraph:03d}"
        else:
            ref = f"{self.volume}.{self.chapter}.{self.paragraph:03d}"
        print(ref, line.strip().split(maxsplit=2)[2], sep="\t")

    def handle_para(self, txt):
        self.paragraph += 1
        if isinstance(self.chapter, int):
            ref = f"{self.volume}.{self.chapter:03d}.{self.paragraph:03d}"
        else:
            ref = f"{self.volume}.{self.chapter}.{self.paragraph:03d}"
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
                if line.startswith("VOLUME ONE"):
                    self.handle_volume(line)
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
                elif line.strip() == "":
                    if txt:
                        self.handle_para(txt)
                        txt = []
                elif line.startswith("VOLUME"):
                    if txt:
                        self.handle_para(txt)
                        txt = []
                    self.handle_volume(line)
                elif line.startswith(" Chapter"):
                    if txt:
                        self.handle_para(txt)
                        txt = []
                    self.handle_chapter(line)
                elif re.match("\d+m\n", line):  # page breaks?
                    if txt:
                        self.handle_para(txt)
                        txt = []
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


p = Parser("pg/1184-0.txt")
p.parse()
