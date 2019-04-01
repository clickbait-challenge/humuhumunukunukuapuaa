from nltk.parse.corenlp import CoreNLPServer
import nltk
import os
from nltk.parse.corenlp import CoreNLPDependencyParser

# The server needs to know the location of the following files:
#   - stanford-corenlp-X.X.X.jar
#   - stanford-corenlp-X.X.X-models.jar
#STANFORD = os.path.join("models", "stanford-corenlp-full-2018-02-27")

nltk.internals.config_java("C:/Program Files/Java/jdk-11.0.2/bin/java.exe")

# Create the server
server = CoreNLPServer(
   os.path.join("C:/Users/nele2/Downloads/stanford-corenlp-full-2018-10-05/stanford-corenlp-3.9.2.jar"),
   os.path.join("C:/Users/nele2/Downloads/stanford-corenlp-full-2018-10-05/stanford-corenlp-3.9.2-models.jar"),    
)

# Start the server in the background
server.start()

parser = CoreNLPDependencyParser()

#head = index of word that a word depends on
# address = index of word itself
# position is 0-indexed where 0-index = "none"

def get_max_length_syntactic_dependencies(text):
    "Returns the maximum distance between the governing and the dependent words \
    in terms of the number of words separating them."
    parse = next(parser.raw_parse(text))
    maxD = 0 # maximum distance between governing and dependent words
    numEntries = len(parse.nodes) # number of entries in dependency tree
    for entry in range(1,  numEntries): # for each term in the sentence
        dist = abs(entry - parse.nodes[entry]["head"])
        if dist > maxD: # update maximum distance
            maxD = dist
    return [maxD]

def get_avg_length_syntactic_dependencies(text):
    "Returns the average distance between the governing and the dependent words \
    in terms of the number of words separating them."
    parse = next(parser.raw_parse(text))
    totalD = 0 # sum of distances between governing and dependent words
    numEntries = len(parse.nodes) # number of entries in dependency tree
    for entry in range(1,  numEntries): # for each term in the sentence
        dist = abs(entry - parse.nodes[entry]["head"])
        totalD += dist
    return [totalD / (numEntries - 1)]

if __name__ == '__main__':
    print(get_max_length_syntactic_dependencies("I put the book in the box on the table"))
    server.stop() # Important!!!!!


>>> from nltk.parse import CoreNLPParser

# Lexical Parser
>>> parser = CoreNLPParser(url='http://localhost:9000')

# Parse tokenized text.
>>> list(parser.parse('What is the airspeed of an unladen swallow ?'.split()))
[Tree('ROOT', [Tree('SBARQ', [Tree('WHNP', [Tree('WP', ['What'])]), Tree('SQ', [Tree('VBZ', ['is']), Tree('NP', [Tree('NP', [Tree('DT', ['the']), Tree('NN', ['airspeed'])]), Tree('PP', [Tree('IN', ['of']), Tree('NP', [Tree('DT', ['an']), Tree('JJ', ['unladen'])])]), Tree('S', [Tree('VP', [Tree('VB', ['swallow'])])])])]), Tree('.', ['?'])])])]

# Parse raw string.
>>> list(parser.raw_parse('What is the airspeed of an unladen swallow ?'))
[Tree('ROOT', [Tree('SBARQ', [Tree('WHNP', [Tree('WP', ['What'])]), Tree('SQ', [Tree('VBZ', ['is']), Tree('NP', [Tree('NP', [Tree('DT', ['the']), Tree('NN', ['airspeed'])]), Tree('PP', [Tree('IN', ['of']), Tree('NP', [Tree('DT', ['an']), Tree('JJ', ['unladen'])])]), Tree('S', [Tree('VP', [Tree('VB', ['swallow'])])])])]), Tree('.', ['?'])])])]

# Neural Dependency Parser
>>> from nltk.parse.corenlp import CoreNLPDependencyParser
>>> dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
>>> parses = dep_parser.parse('What is the airspeed of an unladen swallow ?'.split())
>>> [[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parses]
[[(('What', 'WP'), 'cop', ('is', 'VBZ')), (('What', 'WP'), 'nsubj', ('airspeed', 'NN')), (('airspeed', 'NN'), 'det', ('the', 'DT')), (('airspeed', 'NN'), 'nmod', ('swallow', 'VB')), (('swallow', 'VB'), 'case', ('of', 'IN')), (('swallow', 'VB'), 'det', ('an', 'DT')), (('swallow', 'VB'), 'amod', ('unladen', 'JJ')), (('What', 'WP'), 'punct', ('?', '.'))]]


# Tokenizer
>>> parser = CoreNLPParser(url='http://localhost:9000')
>>> list(parser.tokenize('What is the airspeed of an unladen swallow?'))
['What', 'is', 'the', 'airspeed', 'of', 'an', 'unladen', 'swallow', '?']

# POS Tagger
>>> pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
>>> list(pos_tagger.tag('What is the airspeed of an unladen swallow ?'.split()))
[('What', 'WP'), ('is', 'VBZ'), ('the', 'DT'), ('airspeed', 'NN'), ('of', 'IN'), ('an', 'DT'), ('unladen', 'JJ'), ('swallow', 'VB'), ('?', '.')]

# NER Tagger
>>> ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
>>> list(ner_tagger.tag(('Rami Eid is studying at Stony Brook University in NY'.split())))
[('Rami', 'PERSON'), ('Eid', 'PERSON'), ('is', 'O'), ('studying', 'O'), ('at', 'O'), ('Stony', 'ORGANIZATION'), ('Brook', 'ORGANIZATION'), ('University', 'ORGANIZATION'), ('in', 'O'), ('NY', 'STATE_OR_PROVINCE')]