import glob, json, re, sys

def isValidMessage(datum):
    return 'type' in datum and 'text' in datum and not 'subtype' in datum and datum['type'] == 'message'

def matchesUser(datum):
    return len(sys.argv) <= 1 or ( 'user' in datum and datum['user'] == sys.argv[1]  )


dropMentions = re.compile(r"<@[^>]+>:?")
open('slack-corpus.txt','w+') #Delete and re-create the corpus

for jFile in glob.glob('slack-raw/*/*.json'):
    #print(jFile)
    txt = []
    with open(jFile) as strJson:
        data = json.load(strJson)
        lines = [
            dropMentions.sub('',datum['text']).strip()
            for datum in data
            if isValidMessage(datum) and matchesUser(datum)
        ]
        txt.append("\n".join([line for line in lines if len(line) > 0 ]))
    if(len(txt) >= 0):
        with open('slack-corpus.txt','a') as corpus:
            corpus.write("\n".join(txt))
            corpus.write('\n')

