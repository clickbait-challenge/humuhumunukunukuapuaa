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
parse = next(parser.raw_parse("I put the book in the box on the table"))
print(parse)

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

if __name__ == '__main__':
    print(get_max_length_syntactic_dependencies("I put the book in the box on the table"))
    server.stop()