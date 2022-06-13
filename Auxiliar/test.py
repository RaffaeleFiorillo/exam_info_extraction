from PIL import Image  # adds image processing capabilities
import random
import cv2
from Auxiliar import auxiliary

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


def run():
    for sub in auxiliary.get_sub_directories("enhancements_backups\\segments")[:5]:
        image = Image.open(sub)
        image = remove_pen_marks(image)
        image.show()


run()
