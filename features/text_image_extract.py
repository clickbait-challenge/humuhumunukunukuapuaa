from PIL import Image

import glob
import cv2

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


# the two functions of counting words and chars

def word_count_function(string):
    number_of_words = len(string.split())
    return number_of_words


def character_count_function(string):
    number_of_chars = len(string)
    return number_of_chars


# apply pytesseract on the

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
all_files_with_path = glob.glob(
    "D:/msc/q3/information retrieval/papers to review/nlp project/train4/custom/media/*.jpg") + glob.glob(
    "D:/msc/q3/information retrieval/papers to review/nlp project/train4/custom/media/*.png")
print(len(all_files_with_path))
image_text_no_words = []
image_text_no_chars = []
for i in range(0, len(all_files_with_path)):
    if (pytesseract.image_to_string(Image.open(all_files_with_path[i]))):
        image_text_no_words.append(
            word_count_function(pytesseract.image_to_string(Image.open(all_files_with_path[i]))))
        image_text_no_chars.append(
            character_count_function(pytesseract.image_to_string(Image.open(all_files_with_path[i]))))
    else:
        image_text_no_words.append('0')
        image_text_no_chars.append('0')
with open('text_image_words_no.txt', 'w') as f:
    for item in image_text_no_words:
        f.write("%s\n" % item)
with open('text_image_chars_no.txt', 'w') as f:
    for item in image_text_no_chars:
        f.write("%s\n" % item)
