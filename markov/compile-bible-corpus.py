import glob, json, re, sys

isVerseStarter = re.compile(r"^\d+:\d+")

open('bible-corpus.txt','w+') #Delete and re-create the corpus

with open('king-james.txt','r') as bible:
    def write(txt):
        if len(txt) < 1: return
        with open('bible-corpus.txt','a') as corpus:
            corpus.write(txt)
            corpus.write('\n')

    txt = "";
    for line in bible:
        line = line.strip()
        if len(line) < 1: continue
        if(isVerseStarter.match(line) is not None):
            write(txt)
            txt = isVerseStarter.sub('',line)
        else:
            txt = txt + ' ' + line.strip()


