import glob, json, re, sys

open('shakespeare-corpus.txt','w+') #Delete and re-create the corpus

with open('shakespeare.txt','r') as bible:
    def write(txt):
        if len(txt) < 1: return
        with open('shakespeare-corpus.txt','a') as corpus:
            corpus.write(txt)
            corpus.write('\n')

    txt = "";
    for line in bible:
        line = line.strip()
        if len(line) < 1:
            write(txt)
            txt = line
        else:
            txt = (txt + ' ' + line.strip()).strip()


