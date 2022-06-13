import pytesseract  # will convert the image to text string
from Auxiliar import config
from PIL import Image  # adds image processing capabilities
from textblob import TextBlob
import cv2
import random
import re

pytesseract.pytesseract.tesseract_cmd = config.tesseract_path  # set a customized directory of tesseract

def remove_pen_marks(img):
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = img.getpixel((i, j))
            p_max, p_min = max(pixel), min(pixel)
            # make pixel light-gray if too much red/blue
            if p_max > p_min+20 or (pixel[0] < 100 and pixel[1] < 100 and pixel[2] >= 109):
                pix = max(pixel) + 40
                img.putpixel((i, j), (pix, pix, pix))
    return img

def enhance():
    img = cv2.imread("Auxiliar/backup.png")

    # Convert image to grayscale
    enh = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    enh = cv2.GaussianBlur(enh, (1, 1), 0)
    # Convert image to black and white (using adaptive threshold)
    img = cv2.adaptiveThreshold(enh, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 53, 17)

    # cv2.imwrite(self.backup_dir, img)
    r_number = random.randint(1, 10000)
    cv2.imwrite(f"Auxiliar/enhancements_backups/{r_number}backup.png", img)
    return r_number


class Rmgarbage:
    def too_long(self, string):
        """
        Rule L
        ======

        tests whether the string passed is more than 40 characters, if
        yes. It is garbage!

        :param string: string to be tested
        :returns: either True or False
        """
        return True if len(string) > 15 else False

    def bad_alnum_ratio(self, string):
        """
        Rule A
        ======

        if a string's ratio of alphanumeric characters to total characters is
        less than 50%, the string is garbage

        :param string: string to be tested
        :returns: either True or False
        """

        # matches [^A-Za-z0-9] (^ = not, _ is required)
        pattern = re.compile('[\W_]+')
        alnum_thresholds = {1: 0,     # single chars can be non-alphanumeric
                            2: 0,     # so can doublets
                            3: 0.32,  # at least one of three should be alnum
                            4: 0.24,  # at least one of four should be alnum
                            5: 0.39}  # at least two of five should be alnum

        threshold = alnum_thresholds[len(string)] \
            if len(string) in alnum_thresholds else 0.5

        if len(string) == 0:  # avoid division by zero
            return True
        if float(len(
                pattern.sub('', string)))/len(string) < threshold:
            return True

        return False

    def consecutive_four_identical(self, string):
        """
        Rule R
        ======

        if a string has 4 identical characters in a row, it is garbage

        :param string: string to be tested
        :returns: either True or False
        """
        pattern = re.compile(
            r'((.)\2{3,})')  # matches any 4 consecutive characters
        if pattern.search(string):
            return True

        return False

    def bad_consonant_vowel_ratio(self, string):
        """
        Rule V
        ======
        if a string has nothing but alphabetic characters, look at the
        number of consonants and vowels. If the number of one is less than 10%
        of the number of the other, then the string is garbage.
        This includes a length threshold.

        :param string: string to be tested
        :returns: either True or False
        """
        alpha_string = "".join([char for char in string if char.isalpha()])
        vowel_count = sum(1 for char in alpha_string if char in 'aeiouAEIOU')
        consonant_count = len(alpha_string) - vowel_count

        if consonant_count > 0 and vowel_count > 0:
            ratio = float(vowel_count)/consonant_count
            if ratio < 0.1 or ratio > 10:
                return True
        elif vowel_count == 0 and consonant_count > len('rhythms'):
            return True
        elif consonant_count == 0 and vowel_count > len('IEEE'):
            return True

        return False

    def has_two_distinct_puncts_inside(self, string):
        """
        Rule P
        ======

        Strip off the first and last characters of a string. If there
        are two distinct punctuation characters in the result, then the string
        is garbage

        Customisation
        =============

        stripping off the last TWO characters as false positives
        included those ending with ').' and similar.

        :param string: string to be tested
        :returns: either True or False
        """

        non_alnum_string = ''.join([char for char in string[1:-2] if not char.isalnum()])
        for char in non_alnum_string[1:]:
            if char != non_alnum_string[0]:
                return True
        return False

    def has_uppercase_within_lowercase(self, string):
        """
        Rule C
        ======

        If a string begins and ends with a lowercase letter, then if
        the string contains an uppercase letter anywhere in between, then it
        is removed as garbage.

        Customisation
        =============

        false positive on "needed.The". Exclude fullstop-capital.
        Extra customisation: Exclude hyphen-capital, apostrophe-capital and
        forwardslash-capital

        :param string: string to be tested
        :returns: either True or False
        """
        if (string and string[0].islower() and string[-1].islower()):
            string_middle = string[1:-1]
            for index, char in enumerate(string_middle):
                if char.isupper() and not \
                   (index > 0 and string_middle[index-1] in ".-'"):
                    return True
        return False

    def is_random_letter(self, string):
        return len(string) == 1 and string not in "oaeéOAEÉ"

    def is_garbage(self, string):
        """
        passes the string to check for every rule and if any match is found
        , it returns that rule

        :param string: string to be tested
        :returns: either True or False
        """

        if self.too_long(string):
            return 'L'
        elif self.bad_alnum_ratio(string):
            return 'A'
        elif self.consecutive_four_identical(string):
            return 'R'
        elif self.bad_consonant_vowel_ratio(string):
            return 'V'
        elif self.has_two_distinct_puncts_inside(string):
            return 'P'
        elif self.has_uppercase_within_lowercase(string):
            return 'C'
        elif self.is_random_letter(string):
            return "RL"
        return False

    def clean_sentence(self, sentence):
        good_words = []
        for string in sentence.split(" "):
            if not self.is_garbage(string):
                good_words.append(string)
        return " ".join(good_words)


class IMG:
    backup_dir: str = "backup.png"

    def __init__(self, image: Image):
        self.image: Image = image

    def enhance(self):
        self.image = remove_pen_marks(self.image)
        self.save("Auxiliar/"+self.backup_dir)
        r_number = enhance()
        self.image = Image.open(f"Auxiliar/enhancements_backups/{r_number}{self.backup_dir}")
        # self.image = Image.open(self.backup_dir)

    def extract_text(self):
        self.enhance()  # enhance the image before extracting its content to get better results
        extracted_text = pytesseract.image_to_string(self.image, lang='por')  # converts image to text
        corrected_text = TextBlob(extracted_text)  # corrects the syntax of the words in the extracted text
        # corrected_text = self.tool.correct(corrected_text)  # corrects the grammar of the extracted text
        return corrected_text

    def save(self, directory):
        self.image.save(directory)


class Exam:
    def __init__(self, directory, exercises_coo):
        self.name: str = directory.split("\\")[-1].split(".")[0]
        self.rmgarbage = Rmgarbage()
        print(f"Exam name: {self.name}")
        self.exercises_coo: [[int, int, int, int]] = exercises_coo
        self.exercises_images: [[Image]] = []
        self.get_exercises_images(directory)

    def get_exercises_images(self, directory):
        original = Image.open(directory)
        print(f"Directory: {directory}")
        for i, coo in enumerate(self.exercises_coo):
            print(f"Coordinates: {coo}")
            coo = (coo[1], coo[0], coo[3], coo[2])  # rectify order of coordinates to (left, upper, right, lower)
            cropped = original.crop(coo)
            # cropped.save(f"Results/result{i}_{j}.png")  # -> visualize cropped images
            self.exercises_images.append(IMG(cropped))

    def extract_information(self, save_dir):
        with open(f"{save_dir}/{self.name}.txt", "w") as file:
            for i, image in enumerate(self.exercises_images):
                result = image.extract_text()
                result = self.rmgarbage.clean_sentence(result)
                # file.write(f"Exercise: {i}\n")
                for line in result:
                    file.write(line)
                file.write("\n")
                # file.write("\n-----------------------------------------------------------\n")
