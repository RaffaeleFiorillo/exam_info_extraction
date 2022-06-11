import cv2
import random


def binarize(img):
    # 3. Convert image to grayscale
    enh = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    enh = cv2.GaussianBlur(enh, (1, 1), 0)

    # 4. Convert image to black and white (using adaptive threshold)
    img = cv2.adaptiveThreshold(enh, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 53, 17)
    return img

def remove_pen_marks(img):
    pass

def enhance():
    img = cv2.imread("backup.png")
    # img = remove_pen_marks(img)
    img = binarize(img)
    # cv2.imwrite(self.backup_dir, img)
    r_number = random.randint(1, 10000)
    cv2.imwrite(f"Auxiliar/enhancements_backups/{r_number}backup.png", img)
    return r_number
