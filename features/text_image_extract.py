import glob

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

import ntpath


# the two functions of counting words and chars

def word_count_function(string):
    number_of_words = len(string.split())
    return number_of_words


def character_count_function(string):
    number_of_chars = len(string)
    return number_of_chars


def key_extractor(path):
    return ntpath.basename(path)


# apply pytesseract on the
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_info(media_file):
    all_files_with_path = glob.glob(
        media_file + "/*.jpg") + glob.glob(
        media_file + "/*.png")

    image_meta = {}
    for i in range(0, len(all_files_with_path)):
        s = pytesseract.image_to_string(Image.open(all_files_with_path[i]))
        if s:
            key = key_extractor(all_files_with_path[i])

            image_meta[key] = {'word_count': word_count_function(s), 'character_count': character_count_function(s)}

    return image_meta
