import glob

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
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_info(media_file):
    all_files_with_path = glob.glob(
        media_file + "/*.jpg") + glob.glob(
        media_file + "/*.png")

    image_text_no_words = []
    image_text_no_chars = []
    for i in range(0, len(all_files_with_path)):
        s = pytesseract.image_to_string(Image.open(all_files_with_path[i]))
        if s:
            image_text_no_words.append(
                word_count_function(s))
            image_text_no_chars.append(
                character_count_function(s))
        else:
            image_text_no_words.append('0')
            image_text_no_chars.append('0')
    with open('text_image_words_no.txt', 'w') as f:
        for item in image_text_no_words:
            f.write("%s\n" % item)
    with open('text_image_chars_no.txt', 'w') as f:
        for item in image_text_no_chars:
            f.write("%s\n" % item)
