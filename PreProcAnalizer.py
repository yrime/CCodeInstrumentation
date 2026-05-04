import re

class ppObj:
    def __init__(self, dname, st, end):
        self.directiveName = dname
        self.startOfDirective = st
        self.endOfDirective = end

class PreProcAnalizer:
    PreProcWords = [
        ("INCLUDE", r"#include "),
        ("DEFINE", r"#define "),
        ("IF", r"#if "),
        ("IFDEF", r"#ifdef "),
        ("IFNDEF", r"#ifndef "),
        ("ELSE", r"#else "),
        ("ELIF", r"#elif"),
        ("ENDIF", r"#endif"),
        ("ERROR", r"#error"),
        ("PRAGMA", r"#pragma")
    ]

    def __init__(self):
        self.findedPreProcDirective = []
        self.findedStrings = []

    def checkInStringLiteral(self, i_in, i_out):
        for o in self.findedStrings:
            if (o.startOfDirective < i_in) and (o.endOfDirective > i_out):
                return True
        return False

    def init(self, fname, inc, fcomile):
        self.fname = fname
        self.inc = inc
        self.fcompile = fcompile

    def findStringsLiteral(self, ftext):
        t = 0
        i = 0
        st = False
        while i < len(ftext):
            if ftext[i] in ['\"', '\''] and (ftext[i-1] not in ['\\']):
                if st:
                    st = False
                    self.findedStrings.append(ppObj("STRING", t, i))
                else:
                    t = i
                    st = True
            i = i + 1
        #print(self.findedStrings)
    def findEndPreProcDir(self, startPos, ftext):
        dd = [("END", r"\\[ \t\r]*\n"),
              ("PAS", r"\n")]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in dd)
        for mo in re.finditer(tok_regex, ftext[startPos:]):
            kind = mo.lastgroup
            value = mo.group()
            if kind in {"END"}:
                pass
            elif kind in {"PAS"}:
                if not self.checkInStringLiteral(mo.start(), mo.end()):
                    return mo.end()

    def findPreProcDirective(self, ftext):
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.PreProcWords)
        for mo in re.finditer(tok_regex, ftext):
            kind = mo.lastgroup
            value = mo.group()
            endPos = self.findEndPreProcDir(mo.start(), ftext)
            print("part")
            t = mo.start()
            print(ftext[mo.start(): endPos + t])
            if kind in {"IF", "INCLUDE", "DEFINE", "ERROR", "PRAGMA"}:
                pass
            elif kind in {"IFDEF", "IFNDEF", "ELIF", "ELSE", "ENDIF"}:
                pass
        '''
        ("INCLUDE", r"#include "),
        ("DEFINE", r"#define "),
        ("IF", r"#if "),
        ("IFDEF", r"#ifdef "),
        ("IFNDEF", r"#ifndef "),
        ("ELSE", r"#else "),
        ("ELIF", r"#elif"),
        ("ENDIF", r"#endif"),
        ("ERROR", r"#error"),
        ("PRAGMA", r"#pragma")
        '''
testText = "asd\"adfad(\\\"\"\"\"\n#ifdef sdfsdf\n#if sdf \\ \ndf\\  \nxdf  \" \\ \nggg\n\"hjgk\nljn"

ppa = PreProcAnalizer()
ppa.findStringsLiteral(testText)
ppa.findPreProcDirective(testText)
