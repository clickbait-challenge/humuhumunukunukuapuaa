from nltk.corpus import words
from nltk.corpus import wordnet

import os

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import re

WORDS = set(words.words())


def word_count_function(string):
    if string:
        number_of_words = len(string.split())
    else:
        number_of_words = -1

    return number_of_words


def char_count_function(string):
    if string:
        number_of_words = len(string)
    else:
        number_of_words = -1

    return number_of_words


def keyword_count_function(string):
    if string:
        number_of_words = len(string.split(","))
    else:
        number_of_words = 0

    return number_of_words


class OriginalFeatures():
    def __init__(self, logger, media_path):
        self.logger = logger
        self.media_path = media_path
        self.colnames = ['PostTitleWordsNumber', 'PostTitleCharsNumber',
                         'DiffNoWordsPostTitleAndKeywords', 'DiffNoCharsPostTitleAndKeywords',
                         'RatioNoWordsArticleDescriptionAndPostTitle',
                         'QuestionMarksNoPostTitle', 'RatioNoCharArticleParagraphPostTitle',
                         'RatioNoCharArticleDescriptionPostTitle', 'RatioNoCharArticleTitlePostTitle',
                         'RatioNoWordsArticleTitlePostTitle', 'RatioNoWordsPostImagePostTitle',
                         'DiffCharsPostTitlePostImage', 'RatioCharPostImagePostTitle', 'FormalWordsPostTitle',
                         'RatioNoCharArticleParagraphArticleDescription']
        self.logger.log("Init sentence structure feats extractor with feats list: {}".format(
            self.colnames))

    '''
    @return list of features
    '''

    def compute_features_per_entry(self, data_dict):
        # cached fields
        postText = data_dict['postText'][0]

        # cached results
        wc_postText = word_count_function(postText)
        wc_targetDescription = word_count_function(data_dict['targetDescription'])
        wc_targetTitle = word_count_function(data_dict['targetTitle'])

        cc_postText = char_count_function(postText)
        cc_targetKeywords = char_count_function(data_dict['targetKeywords'])
        cc_targetParagraphs = char_count_function(data_dict['targetParagraphs'])
        cc_targetDescription = char_count_function(data_dict['targetDescription'])
        cc_targetTitle = char_count_function(data_dict['targetTitle'])

        kc_targetKeywords = keyword_count_function(data_dict['targetKeywords'])

        cc_im = 0
        wc_im = 0
        if data_dict['postMedia']:
            # should be fine even with //
            s = pytesseract.image_to_string(Image.open(
                os.path.join(self.media_path, data_dict['postMedia'][0])))

            if s:
                wc_im = word_count_function(s)
                cc_im = char_count_function(s)

        # format words count
        lower_case_postText = postText.lower()
        words = re.findall(r"[\w']+", lower_case_postText)
        formal_words = 0
        for word in words:
            if word in WORDS or wordnet.synsets(word):
                formal_words += 1

        # load results
        results = [
            # # Number of words in post title
            # def post_title_words(data):
            wc_postText,

            # # Number of characters in post title
            # def post_title_chars(data):
            cc_postText,

            # # Difference number of words post title and article keywords.
            # def diff_words_title_keywords(data):
            abs(wc_postText - kc_targetKeywords),

            # # Difference number of characters post title and article keywords
            # def diff_chars_title_keywords(data):
            abs(cc_postText - cc_targetKeywords) if cc_targetKeywords != -1 else cc_postText,

            # # Ratio number of words article description and post title
            # def ratio_words_descr_title(data):
            wc_targetDescription / wc_postText if wc_targetDescription != -1 else -1,

            # # Number of question marks in post title
            # def question_marks_title(data):
            postText.count('?'),

            # # Number of characters ratio article paragraphs and post title
            # def ratio_paragraphs_title(data):
            cc_targetParagraphs / cc_postText if cc_targetParagraphs != -1 else -1,

            # # Number of characters ratio article description and post title
            # def ratio_description_title(data):
            cc_targetDescription / cc_postText if cc_targetDescription != -1 else -1,

            # # Number of characters ratio article title and post title
            # def ratio_article_title_post_title(data):
            cc_targetTitle / cc_postText if cc_targetTitle != -1 else -1,

            # # Number of words ratio article title and post title
            # def ratio_words_article_title_post_title(data):
            wc_targetTitle / wc_postText if wc_targetTitle != -1 else -1,

            # # Ratio words in post image and post title
            # def ratio_words_image_title(data, image_meta):
            wc_im / wc_postText if wc_im != 0 else 0,

            # # Difference characters post title and image text
            # def diff_chars_title_image(data, image_meta):
            abs(cc_im - cc_postText),

            # # ratio characters post image text and post title
            # def ratio_chars_image_title(data, image_meta):
            cc_im / cc_postText if cc_im != 0 else 0,

            # # check if formal word
            # def check_formal_words_no(data):
            formal_words,

            # # Number of characters ratio article paragraphs and article description
            # def ratio_paragraphs_description(data):
            cc_targetParagraphs / cc_targetDescription if (cc_targetParagraphs != -1 and cc_targetDescription != -1)
            else -1

        ] if postText else [
            # # Number of words in post title
            # def post_title_words(data):
            wc_postText,

            # # Number of characters in post title
            # def post_title_chars(data):
            cc_postText,

            # # Difference number of words post title and article keywords.
            # def diff_words_title_keywords(data):
            abs(wc_postText - kc_targetKeywords),

            # # Difference number of characters post title and article keywords
            # def diff_chars_title_keywords(data):
            abs(cc_postText - cc_targetKeywords) if cc_targetKeywords != -1 else cc_postText,

            # # Ratio number of words article description and post title
            # def ratio_words_descr_title(data):
            -1,

            # # Number of question marks in post title
            # def question_marks_title(data):
            postText.count('?'),

            # # Number of characters ratio article paragraphs and post title
            # def ratio_paragraphs_title(data):
            -1,

            # # Number of characters ratio article description and post title
            # def ratio_description_title(data):
            -1,

            # # Number of characters ratio article title and post title
            # def ratio_article_title_post_title(data):
            -1,

            # # Number of words ratio article title and post title
            # def ratio_words_article_title_post_title(data):
            -1,

            # # Ratio words in post image and post title
            # def ratio_words_image_title(data, image_meta):
            0,

            # # Difference characters post title and image text
            # def diff_chars_title_image(data, image_meta):
            abs(cc_im - cc_postText),

            # # ratio characters post image text and post title
            # def ratio_chars_image_title(data, image_meta):
            0,

            # # check if formal word
            # def check_formal_words_no(data):
            formal_words,

            # # Number of characters ratio article paragraphs and article description
            # def ratio_paragraphs_description(data):
            cc_targetParagraphs / cc_targetDescription if cc_targetParagraphs * cc_targetDescription != 0 else -1
        ]

        return results

    def end_computing_features(self):
        return self.colnames
