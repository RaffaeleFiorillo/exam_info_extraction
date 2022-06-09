import pytesseract  # will convert the image to text string
from Auxiliar import config
from PIL import Image  # adds image processing capabilities
import cv2

pytesseract.pytesseract.tesseract_cmd = config.tesseract_path  # set a customized directory of tesseract

class IMG:
    backup_dir: str = "backup.png"

    def __init__(self, image: Image):
        self.image: Image = image

    def enhance(self):
        self.save(self.backup_dir)
        img = cv2.imread(self.backup_dir)
        # 3. Convert image to grayscale
        enh = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        enh = cv2.GaussianBlur(enh, (1, 1), 0)

        # 4. Convert image to black and white (using adaptive threshold)
        img = cv2.adaptiveThreshold(enh, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 71, 7)
        cv2.imwrite(self.backup_dir, img)
        self.image = Image.open(self.backup_dir)

    def extract_text(self):
        self.enhance()  # enhance the image before extracting its content to get better results
        return pytesseract.image_to_string(self.image, lang='por')  # converts image to text

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
                file.write(f"Exercise: {i}")
                for line in result:
                    file.write(line)
                file.write("\n-----------------------------------------------------------\n")
