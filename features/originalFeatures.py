from nltk.corpus import words

from nltk.corpus import wordnet

import glob

try:
    from PIL import Image
except ImportError:
    import Image
import re
from pandas import DataFrame

# Helpers:

def word_count_function(string):
    if (string):
        number_of_words = len(string.split())
    else:
        number_of_words = -1
    return number_of_words


def character_count_function(string):
    if (string):
        number_of_chars = len(string)
    else:
        number_of_chars = -1
    return number_of_chars


def keyword_count(string):
    if (string):
        number_of_keywords = len(string.split(','))
    else:
        number_of_keywords = -1
    return number_of_keywords


def read_from_file(filename):
    list = []
    file = open(filename, 'r')
    list.append(file.readlines())
    return list


def get_id_data(data, media_location):
    id_data = []
    for i in range(0, len(data)):
        id_data.append(str(data[i]['id']))
    return id_data


# Features:


# Number of words in post title.

def post_title_words(data, media_location):
    post_title_words_vector = []
    for i in range(0, len(data)):
        post_title_words_vector.append(word_count_function(data[i]['postText'][0]))
    return post_title_words_vector


# print(post_title_words())

# print(id_data)


# Difference number of words post title and article keywords.

def diff_words_title_keywords(data, media_location):
    diff_words_title_keywords_vector = []
    for i in range(0, len(data)):
        if (data[i]['targetKeywords']):
            diff_words_title_keywords_vector.append(
                abs(word_count_function(data[i]['postText'][0]) - keyword_count(data[i]['targetKeywords'])))
        else:
            diff_words_title_keywords_vector.append(word_count_function(data[i]['postText'][0]))
    return diff_words_title_keywords_vector


# Difference number of characters post title and article keywords

def diff_chars_title_keywords(data, media_location):
    diff_chars_title_keywords_vector = []
    for i in range(0, len(data)):
        if (data[i]['targetKeywords']):
            diff_chars_title_keywords_vector.append(abs(
                character_count_function(data[i]['postText'][0]) - character_count_function(
                    data[i]['targetKeywords'])))
        else:
            diff_chars_title_keywords_vector.append(character_count_function(data[i]['postText'][0]))
    return diff_chars_title_keywords_vector


# Ratio number of words article description and post title

def ratio_words_descr_title(data, media_location):
    ratio_words_descr_title_vector = []

    for i in range(0, len(data)):
        if (data[i]['targetDescription'] and data[i]['postText']):
            ratio_words_descr_title_vector.append(
                word_count_function(data[i]['targetDescription']) / word_count_function(data[i]['postText'][0]))
        else:
            ratio_words_descr_title_vector.append(-1)
    return ratio_words_descr_title_vector


# Number of question marks in post title

def question_marks_title(data, media_location):
    question_marks_title_vector = []
    for i in range(0, len(data)):
        question_marks_title_vector.append(data[i]['postText'][0].count('?'))
    return question_marks_title_vector


# Number of characters in post title

def post_title_chars(data, media_location):
    post_title_chars_vector = []
    for i in range(0, len(data)):
        post_title_chars_vector.append(character_count_function(data[i]['postText'][0]))
    return post_title_chars_vector


# Number of characters ratio article paragraphs and post title

def ratio_paragraphs_title(data, media_location):
    ratio_paragraphs_title_vector = []
    for i in range(0, len(data)):
        if (data[i]['targetParagraphs'] and data[i]['postText'][0]):
            ratio_paragraphs_title_vector.append(
                character_count_function(data[i]['targetParagraphs']) / character_count_function(
                    data[i]['postText'][0]))
        else:
            ratio_paragraphs_title_vector.append(-1)
    return ratio_paragraphs_title_vector


# Number of characters ratio article description and post title

def ratio_description_title(data, media_location):
    ratio_description_title_vector = []
    for i in range(0, len(data)):
        if (data[i]['postText'][0] and str(data[i]['targetDescription'])):
            ratio_description_title_vector.append(
                character_count_function(data[i]['targetDescription']) / character_count_function(
                    data[i]['postText'][0]))
        else:
            ratio_description_title_vector.append(-1)
    print(len(ratio_description_title_vector))
    return ratio_description_title_vector


# Number of characters ratio article paragraphs and article description


def ratio_paragraphs_description(data, media_location):
    ratio_paragraphs_description_vector = []

    for i in range(0, len(data)):
        if (data[i]['targetParagraphs'] and data[i]['targetDescription']):
            ratio_paragraphs_description_vector.append(
                character_count_function(data[i]['targetParagraphs']) / character_count_function(
                    data[i]['targetDescription']))
        else:
            ratio_paragraphs_description_vector.append(-1)
    return ratio_paragraphs_description_vector


# Number of characters ratio article title and post title


def ratio_article_title_post_title(data, media_location):
    ratio_article_title_post_title_vector = []
    for i in range(0, len(data)):
        if (data[i]['targetTitle'] and data[i]['postText'][0]):
            ratio_article_title_post_title_vector.append(
                character_count_function(data[i]['targetTitle']) / character_count_function(data[i]['postText'][0]))
        else:
            ratio_article_title_post_title_vector.append(-1)
    return ratio_article_title_post_title_vector


# Number of words ratio article title and post title


def ratio_words_article_title_post_title(data, media_location):
    ratio_words_article_title_post_title_vector = []
    for i in range(0, len(data)):
        if (data[i]['targetTitle'] and data[i]['postText'][0]):
            ratio_words_article_title_post_title_vector.append(
                word_count_function(data[i]['targetTitle']) / word_count_function(data[i]['postText'][0]))
        else:
            ratio_words_article_title_post_title_vector.append(-1)
    return ratio_words_article_title_post_title_vector


# Ratio words in post image and post title


def ratio_words_image_title(data, media_location):
    # preprocess data from file and convert it into int format
    text_image_words_no_str = []
    text_image_words_no = []
    text_image_words_no_str = read_from_file('text_image_words_no.txt')
    for i in range(0, len(text_image_words_no_str[0])):
        text_image_words_no.append(int(text_image_words_no_str[0][i]))
    # names of pictures from media (both jpg and png)
    all_files_with_path = glob.glob(
        media_location + ".jpg") + glob.glob(
        media_location + ".png")
    # find each corresponding image from the dataset
    all_text_image_no = []
    count = 0
    for i in range(0, len(data)):
        if (data[i]['postMedia']):
            for j in range(0, len(all_files_with_path)):
                if (str(data[i]['postMedia'][0]) in all_files_with_path[j]):
                    all_text_image_no.append(text_image_words_no[j])
        else:
            all_text_image_no.append(0)
            count = count + 1
    ratio_words_image_title_vector = []

    # make ratio
    for i in range(0, len(data)):
        ratio_words_image_title_vector.append(all_text_image_no[i] / character_count_function(data[i]['postText'][0]))
    return ratio_words_image_title_vector


# Difference characters post title and image text

def diff_chars_title_image(data, media_location):
    # preprocess data from file and convert it into int format
    text_image_words_no_str = []
    text_image_words_no = []
    text_image_words_no_str = read_from_file('text_image_words_no.txt')

    for i in range(0, len(text_image_words_no_str[0])):
        text_image_words_no.append(int(text_image_words_no_str[0][i]))

    # names of pictures from media (both jpg and png)
    all_files_with_path = glob.glob(
        media_location + ".jpg") + glob.glob(
        media_location + ".png")
    # find each corresponding image from the dataset
    all_text_image_no = []
    count = 0

    for i in range(0, len(data)):
        if (data[i]['postMedia']):
            for j in range(0, len(all_files_with_path)):
                # print(data[i]['postMedia'])
                # print(data[i]['postMedia'][0])
                if (str(data[i]['postMedia'][0]) in all_files_with_path[j]):
                    all_text_image_no.append(text_image_words_no[j])
        else:
            all_text_image_no.append(0)
            count = count + 1
    diff_chars_title_image_vector = []
    # make ratio
    for i in range(0, len(data)):
        diff_chars_title_image_vector.append(
            abs(all_text_image_no[i] - character_count_function(data[i]['postText'][0])))
    return diff_chars_title_image_vector


# ratio characters post image text and post title

def ratio_chars_image_title(data, media_location):
    # preprocess data from file and convert it into int format
    text_image_words_no_str = []
    text_image_words_no = []
    text_image_words_no_str = read_from_file('text_image_words_no.txt')
    for i in range(0, len(text_image_words_no_str[0])):
        text_image_words_no.append(int(text_image_words_no_str[0][i]))
    # names of pictures from media (both jpg and png)
    all_files_with_path = glob.glob(
        media_location + ".jpg") + glob.glob(
        media_location + ".png")
    # find each corresponding image from the dataset
    all_text_image_no = []
    count = 0
    for i in range(0, len(data)):
        if (data[i]['postMedia']):
            for j in range(0, len(all_files_with_path)):
                if (str(data[i]['postMedia'][0]) in all_files_with_path[j]):
                    all_text_image_no.append(text_image_words_no[j])
        else:
            all_text_image_no.append(0)
            count = count + 1
    diff_chars_title_image_vector = []
    # make ratio chars post image and post title
    ratio_chars_image_title_vector = []
    for i in range(0, len(data)):
        if (data[i]['postMedia'] and data[i]['postText'][0]):
            ratio_chars_image_title_vector.append(
                all_text_image_no[i] / character_count_function(data[i]['postText'][0]))
        else:
            ratio_chars_image_title_vector.append(0)
    return ratio_chars_image_title_vector


# check if formal word

def check_formal_words_no(data, media_location):
    # take each post title

    formal_words_title_no = []

    for j in range(0, len(data)):
        DATA = data[j]['postText'][0]

        # split data in words
        split_data = re.findall(r"[\w']+", DATA)
        count = 0
        for i in range(0, len(split_data)):
            word_to_test = split_data[i].lower()
            if (word_to_test in words.words() or wordnet.synsets(word_to_test)):
                count = count + 1

        formal_words_title_no.append(count)

    return formal_words_title_no


# # print(check_formal_words_no())
#
# print(len(get_id_data()))
# print(len(post_title_words()))
# print(len(post_title_chars()))
# print(len(diff_words_title_keywords()))
# print(len(diff_chars_title_keywords()))
# print(len(ratio_words_descr_title()))
# print(len(question_marks_title()))
# print(len(ratio_paragraphs_title()))
# print(len(ratio_article_title_post_title()))
# print(len(ratio_words_image_title()))
# print(len(diff_chars_title_image()))
# print(len(ratio_chars_image_title()))
# print(len(ratio_paragraphs_description()))
# # print(len(check_formal_words_no()))
# print(len(ratio_words_image_title()))
#

def get_original_features(data, media_location):
    original_features = [
        post_title_words(data, media_location),
        post_title_chars(data, media_location),
        diff_words_title_keywords(data, media_location),
        diff_chars_title_keywords(data, media_location),
        ratio_words_descr_title(data, media_location),
        question_marks_title(data, media_location),
        ratio_paragraphs_title(data, media_location),
        ratio_description_title(data, media_location),
        ratio_article_title_post_title(data, media_location),
        ratio_words_article_title_post_title(data, media_location),
        ratio_words_image_title(data, media_location),
        diff_chars_title_image(data, media_location),
        ratio_chars_image_title(data, media_location),
        check_formal_words_no(data, media_location),
        ratio_paragraphs_description(data, media_location)
    ]

    return original_features


def meld_with_original_features(data, media_location, store):
    original_features = get_original_features(data, media_location)
    for i in range(0, len(store)):
        container = store[i]
        for original_features_array in original_features:
            container.append(original_features_array[i])


column_names = ['PostTitleWordsNumber', 'PostTitleCharsNumber', 'DiffNoWordsPostTitleAndKeywords',
                'DiffNoCharsPostTitleAndKeywords', 'RatioNoWordsArticleDescriptionAndPostTitle',
                'QuestionMarksNoPostTitle', 'RatioNoCharArticleParagraphPostTitle',
                'RatioNoCharArticleDescriptionPostTitle', 'RatioNoCharArticleTitlePostTitle',
                'RatioNoWordsArticleTitlePostTitle', 'RatioNoWordsPostImagePostTitle',
                'DiffCharsPostTitlePostImage', 'RatioCharPostImagePostTitle', 'FormalWordsPostTitle',
                'RatioNoCharArticleParagraphArticleDescription']


def export():
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
