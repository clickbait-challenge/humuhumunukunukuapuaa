import json
import os
from nltk.corpus import words

from nltk.corpus import wordnet

from PIL import Image
import glob
import cv2

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import re
from pandas import DataFrame

import numpy as np

CWD = os.getcwd()
JSON_CONFIG_FILE_PATH = '%s/%s' % (CWD, 'instances_modified.jsonl');
CONFIG_PROPERTIES = {}
with open(JSON_CONFIG_FILE_PATH, 'r', encoding="utf8") as f:
    data = [json.loads(line) for line in f]


# Helpers:

def word_count_function(string):
    if (string):
        number_of_words = len(string.split())
    else:
        number_of_words = -1;
    return number_of_words;


def character_count_function(string):
    if (string):
        number_of_chars = len(string);
    else:
        number_of_chars = -1;
    return number_of_chars;


def keyword_count(string):
    if (string):
        number_of_keywords = len(string.split(','))
    else:
        number_of_keywords = -1;
    return number_of_keywords;


def read_from_file(filename):
    list = [];
    file = open(filename, 'r')
    list.append(file.readlines())
    return list;


def get_id_data():
    id_data = []
    for i in range(0, len(data)):
        id_data.append(str(data[i]['id']))
    return id_data;


# Features:


# Number of words in post title.

def post_title_words():
    post_title_words_vector = [];
    for i in range(0, len(data)):
        post_title_words_vector.append(word_count_function(data[i]['postText'][0]));
    return post_title_words_vector;


# print(post_title_words());

# print(id_data)


# Difference number of words post title and article keywords.

def diff_words_title_keywords():
    diff_words_title_keywords_vector = []
    for i in range(0, len(data)):
        if (data[i]['targetKeywords']):
            diff_words_title_keywords_vector.append(
                abs(word_count_function(data[i]['postText'][0]) - keyword_count(data[i]['targetKeywords'])));
        else:
            diff_words_title_keywords_vector.append(word_count_function(data[i]['postText'][0]));
    return diff_words_title_keywords_vector;


# Difference number of characters post title and article keywords

def diff_chars_title_keywords():
    diff_chars_title_keywords_vector = []
    for i in range(0, len(data)):
        if (data[i]['targetKeywords']):
            diff_chars_title_keywords_vector.append(abs(
                character_count_function(data[i]['postText'][0]) - character_count_function(
                    data[i]['targetKeywords'])));
        else:
            diff_chars_title_keywords_vector.append(character_count_function(data[i]['postText'][0]));
    return diff_chars_title_keywords_vector;


# Ratio number of words article description and post title

def ratio_words_descr_title():
    ratio_words_descr_title_vector = [];

    for i in range(0, len(data)):
        if (data[i]['targetDescription'] and data[i]['postText']):
            ratio_words_descr_title_vector.append(
                word_count_function(data[i]['targetDescription']) / word_count_function(data[i]['postText'][0]))
        else:
            ratio_words_descr_title_vector.append(-1);
    return ratio_words_descr_title_vector;


# Number of question marks in post title

def question_marks_title():
    question_marks_title_vector = [];
    for i in range(0, len(data)):
        question_marks_title_vector.append(data[i]['postText'][0].count('?'));
    return question_marks_title_vector;


# Number of characters in post title

def post_title_chars():
    post_title_chars_vector = [];
    for i in range(0, len(data)):
        post_title_chars_vector.append(character_count_function(data[i]['postText'][0]));
    return post_title_chars_vector;


# Number of characters ratio article paragraphs and post title

def ratio_paragraphs_title():
    ratio_paragraphs_title_vector = [];
    for i in range(0, len(data)):
        if (data[i]['targetParagraphs'] and data[i]['postText'][0]):
            ratio_paragraphs_title_vector.append(
                character_count_function(data[i]['targetParagraphs']) / character_count_function(
                    data[i]['postText'][0]));
        else:
            ratio_paragraphs_title_vector.append(-1)
    return ratio_paragraphs_title_vector;


# Number of characters ratio article description and post title

def ratio_description_title():
    ratio_description_title_vector = [];
    for i in range(0, len(data)):
        if (data[i]['postText'][0] and str(data[i]['targetDescription'])):
            ratio_description_title_vector.append(
                character_count_function(data[i]['targetDescription']) / character_count_function(
                    data[i]['postText'][0]));
        else:
            ratio_description_title_vector.append(-1);
    print(len(ratio_description_title_vector))
    return ratio_description_title_vector;


# Number of characters ratio article paragraphs and article description


def ratio_paragraphs_description():
    ratio_paragraphs_description_vector = [];

    for i in range(0, len(data)):
        if (data[i]['targetParagraphs'] and data[i]['targetDescription']):
            ratio_paragraphs_description_vector.append(
                character_count_function(data[i]['targetParagraphs']) / character_count_function(
                    data[i]['targetDescription']));
        else:
            ratio_paragraphs_description_vector.append(-1)
    return ratio_paragraphs_description_vector;


# Number of characters ratio article title and post title


def ratio_article_title_post_title():
    ratio_article_title_post_title_vector = [];
    for i in range(0, len(data)):
        if (data[i]['targetTitle'] and data[i]['postText'][0]):
            ratio_article_title_post_title_vector.append(
                character_count_function(data[i]['targetTitle']) / character_count_function(data[i]['postText'][0]));
        else:
            ratio_article_title_post_title_vector.append(-1)
    return ratio_article_title_post_title_vector;


# Number of words ratio article title and post title


def ratio_words_article_title_post_title():
    ratio_words_article_title_post_title_vector = [];
    for i in range(0, len(data)):
        if (data[i]['targetTitle'] and data[i]['postText'][0]):
            ratio_words_article_title_post_title_vector.append(
                word_count_function(data[i]['targetTitle']) / word_count_function(data[i]['postText'][0]));
        else:
            ratio_words_article_title_post_title_vector.append(-1)
    return ratio_words_article_title_post_title_vector;


# Ratio words in post image and post title


def ratio_words_image_title():
    # preprocess data from file and convert it into int format
    text_image_words_no_str = [];
    text_image_words_no = []
    text_image_words_no_str = read_from_file('text_image_words_no.txt')
    for i in range(0, len(text_image_words_no_str[0])):
        text_image_words_no.append(int(text_image_words_no_str[0][i]));
    # names of pictures from media (both jpg and png)
    all_files_with_path = glob.glob(
        "D:/msc/q3/information retrieval/papers to review/nlp project/train4/custom/media/*.jpg") + glob.glob(
        "D:/msc/q3/information retrieval/papers to review/nlp project/train4/custom/media/*.png")
    # find each corresponding image from the dataset
    all_text_image_no = [];
    count = 0;
    for i in range(0, len(data)):
        if (data[i]['postMedia']):
            for j in range(0, len(all_files_with_path)):
                if (str(data[i]['postMedia'][0]) in all_files_with_path[j]):
                    all_text_image_no.append(text_image_words_no[j]);
        else:
            all_text_image_no.append(0);
            count = count + 1;
    ratio_words_image_title_vector = [];

    # make ratio
    for i in range(0, len(data)):
        ratio_words_image_title_vector.append(all_text_image_no[i] / character_count_function(data[i]['postText'][0]));
    return ratio_words_image_title_vector;


# Difference characters post title and image text

def diff_chars_title_image():
    # preprocess data from file and convert it into int format
    text_image_words_no_str = [];
    text_image_words_no = []
    text_image_words_no_str = read_from_file('text_image_words_no.txt')

    for i in range(0, len(text_image_words_no_str[0])):
        text_image_words_no.append(int(text_image_words_no_str[0][i]));

    # names of pictures from media (both jpg and png)
    all_files_with_path = glob.glob(
        "D:/msc/q3/information retrieval/papers to review/nlp project/train4/custom/media/*.jpg") + glob.glob(
        "D:/msc/q3/information retrieval/papers to review/nlp project/train4/custom/media/*.png")
    # find each corresponding image from the dataset
    all_text_image_no = [];
    count = 0;

    for i in range(0, len(data)):
        if (data[i]['postMedia']):
            for j in range(0, len(all_files_with_path)):
                # print(data[i]['postMedia'])
                # print(data[i]['postMedia'][0])
                if (str(data[i]['postMedia'][0]) in all_files_with_path[j]):
                    all_text_image_no.append(text_image_words_no[j]);
        else:
            all_text_image_no.append(0);
            count = count + 1;
    diff_chars_title_image_vector = [];
    # make ratio
    for i in range(0, len(data)):
        diff_chars_title_image_vector.append(
            abs(all_text_image_no[i] - character_count_function(data[i]['postText'][0])));
    return diff_chars_title_image_vector;


# ratio characters post image text and post title

def ratio_chars_image_title():
    # preprocess data from file and convert it into int format
    text_image_words_no_str = [];
    text_image_words_no = []
    text_image_words_no_str = read_from_file('text_image_words_no.txt')
    for i in range(0, len(text_image_words_no_str[0])):
        text_image_words_no.append(int(text_image_words_no_str[0][i]));
    # names of pictures from media (both jpg and png)
    all_files_with_path = glob.glob(
        "D:/msc/q3/information retrieval/papers to review/nlp project/train4/custom/media/*.jpg") + glob.glob(
        "D:/msc/q3/information retrieval/papers to review/nlp project/train4/custom/media/*.png")
    # find each corresponding image from the dataset
    all_text_image_no = [];
    count = 0;
    for i in range(0, len(data)):
        if (data[i]['postMedia']):
            for j in range(0, len(all_files_with_path)):
                if (str(data[i]['postMedia'][0]) in all_files_with_path[j]):
                    all_text_image_no.append(text_image_words_no[j]);
        else:
            all_text_image_no.append(0);
            count = count + 1;
    diff_chars_title_image_vector = [];
    # make ratio chars post image and post title
    ratio_chars_image_title_vector = [];
    for i in range(0, len(data)):
        if (data[i]['postMedia'] and data[i]['postText'][0]):
            ratio_chars_image_title_vector.append(
                all_text_image_no[i] / character_count_function(data[i]['postText'][0]));
        else:
            ratio_chars_image_title_vector.append(0)
    return ratio_chars_image_title_vector;


# check if formal word

def check_formal_words_no():
    # take each post title

    formal_words_title_no = [];

    for j in range(0, len(data)):
        DATA = data[j]['postText'][0]

        # split data in words
        split_data = re.findall(r"[\w']+", DATA)
        count = 0;
        for i in range(0, len(split_data)):
            word_to_test = split_data[i].lower()
            if (word_to_test in words.words() or wordnet.synsets(word_to_test)):
                count = count + 1;

        formal_words_title_no.append(count);

    return formal_words_title_no;


# print(check_formal_words_no())

print(len(get_id_data()))
print(len(post_title_words()))
print(len(post_title_chars()))
print(len(diff_words_title_keywords()))
print(len(diff_chars_title_keywords()))
print(len(ratio_words_descr_title()))
print(len(question_marks_title()))
print(len(ratio_paragraphs_title()))
print(len(ratio_article_title_post_title()))
print(len(ratio_words_image_title()))
print(len(diff_chars_title_image()))
print(len(ratio_chars_image_title()))
print(len(ratio_paragraphs_description()))
# print(len(check_formal_words_no()))
print(len(ratio_words_image_title()))

original_features = {'id': get_id_data(),
                     'PostTitleWordsNumber': post_title_words(),
                     'PostTitleCharsNumber': post_title_chars(),
                     'DiffNoWordsPostTitleAndKeywords': diff_words_title_keywords(),
                     'DiffNoCharsPostTitleAndKeywords': diff_chars_title_keywords(),
                     'RatioNoWordsArticleDescriptionAndPostTitle': ratio_words_descr_title(),
                     'QuestionMarksNoPostTitle': question_marks_title(),
                     'RatioNoCharArticleParagraphPostTitle': ratio_paragraphs_title(),
                     'RatioNoCharArticleDescriptionPostTitle': ratio_description_title(),
                     'RatioNoCharArticleTitlePostTitle': ratio_article_title_post_title(),
                     'RatioNoWordsArticleTitlePostTitle': ratio_words_article_title_post_title(),
                     'RatioNoWordsPostImagePostTitle': ratio_words_image_title(),
                     'DiffCharsPostTitlePostImage': diff_chars_title_image(),
                     'RatioCharPostImagePostTitle': ratio_chars_image_title(),
                     'FormalWordsPostTitle': check_formal_words_no(),
                     'RatioNoCharArticleParagraphArticleDescription': ratio_paragraphs_description()
                     }

df = DataFrame(original_features,
               columns=['id', 'PostTitleWordsNumber', 'PostTitleCharsNumber', 'DiffNoWordsPostTitleAndKeywords',
                        'DiffNoCharsPostTitleAndKeywords', 'RatioNoWordsArticleDescriptionAndPostTitle',
                        'QuestionMarksNoPostTitle', 'RatioNoCharArticleParagraphPostTitle',
                        'RatioNoCharArticleDescriptionPostTitle', 'RatioNoCharArticleTitlePostTitle',
                        'RatioNoWordsArticleTitlePostTitle', 'RatioNoWordsPostImagePostTitle',
                        'DiffCharsPostTitlePostImage', 'RatioCharPostImagePostTitle', 'FormalWordsPostTitle',
                        'RatioNoCharArticleParagraphArticleDescription'])
print(df)
export_csv = df.to_csv(
    r'D:\msc\q3\information retrieval\papers to review\nlp project\train4\custom\originalFeaturesTrainMihai.csv',
    index=None, header=True)
