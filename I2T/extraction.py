import pytesseract  # will convert the image to text string
from Auxiliar import config
import enhancement
from PIL import Image  # adds image processing capabilities
from textblob import TextBlob

pytesseract.pytesseract.tesseract_cmd = config.tesseract_path  # set a customized directory of tesseract

class IMG:
    backup_dir: str = "backup.png"

    def __init__(self, image: Image):
        self.image: Image = image

    def enhance(self):
        # enhance.remove_pen_marks()
        self.save(self.backup_dir)
        r_number = enhancement.enhance()
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
        print(f"Exam name: {self.name}")
        print(f"Coo: {exercises_coo}")
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
                # file.write(f"Exercise: {i}\n")
                for line in result:
                    file.write(line)
                file.write("\n")
                # file.write("\n-----------------------------------------------------------\n")
