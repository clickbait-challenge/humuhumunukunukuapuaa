import json_lines
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import opinion_lexicon, stopwords
#from nltk.parse.stanford import StanfordDependencyParser
#import sys
#sys.path.insert(0, C:/Users/nele2/Downloads/Stanford-parser-python-r22186/src/stanford_parser/)

validationInstances = []
validationTruth = []
trainInstances = []
trainTruth = []

with open('C:/Users/nele2/Desktop/clickbait17-validation-170630/instances.jsonl', 'rb') as f: # opening file in binary(rb) mode    
   for item in json_lines.reader(f):
       validationInstances.append(item)
       
with open('C:/Users/nele2/Desktop/clickbait17-validation-170630/truth.jsonl', 'rb') as f: # opening file in binary(rb) mode    
   for item in json_lines.reader(f):
       validationTruth.append(item)
       
with open('C:/Users/nele2/Desktop/clickbait17-train-170331/instances.jsonl', 'rb') as f: # opening file in binary(rb) mode    
   for item in json_lines.reader(f):
       trainInstances.append(item)
       
with open('C:/Users/nele2/Desktop/clickbait17-train-170331/truth.jsonl', 'rb') as f: # opening file in binary(rb) mode    
   for item in json_lines.reader(f):
       trainTruth.append(item)
       
vader_analyzer = SentimentIntensityAnalyzer()

downworthy = set()
f = open("C:/Users/nele2/Desktop/AppliedNLP_PaperRep/Downworthy.txt", 'r')
for term in f:
    downworthy.add(term.rstrip().lower()) # remove space + convert to lower case
f.close()

def get_vader_scores(text):
    "Returns a list of Vader sentiment scores: negative, neutral, positive."
    sentiment_scores = vader_analyzer.polarity_scores(text)
    return [sentiment_scores["neg"], sentiment_scores["neu"], sentiment_scores["pos"]]


def get_opinion_lexicon(text):
    "Returns number of positive and negative words."
    pos_opinion_count = len(set(opinion_lexicon.positive()) & set(text.split()))
    neg_opinion_count = len(set(opinion_lexicon.negative()) & set(text.split()))
    return [pos_opinion_count, neg_opinion_count]

def get_average_word_length(text):
    "Returns the average length of words in a text."
    setOfWords = set(text.split()) # set of words in the text
    total_length = 0
    for word in setOfWords: # for each word
        total_length += len(word)
    return [total_length / len(setOfWords)]

def get_start_digit(text):
    "Returns True if the first character of the text is a digit."
    return [str.isdigit(text[0])]

def get_num_stopwords(text):
    "Returns the number of stop words in a text."
    setOfWords = set(text.split()) # set of words in text
    total = 0
    for word in setOfWords: # for each word in text
        if word in stopwords.words('english'): # check if word is a stop word
            total += 1
    return [total]

def get_common_bit_phrase(text):
    "Returns whether a text contains a common bait phrase."
    for phrase in downworthy: # for each bait phrase
        if phrase in text.lower(): # check if phrase is in lower-case version of text
            return [1]
    return [0]

if __name__ == '__main__':
    
    #res = get_length_syntactic_dependencies("hu")
    #print(res)
    res = get_num_stopwords("I like the cow and the dog kind of much.")
    print(res)