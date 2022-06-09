import extraction as e


if __name__ == "__main__":
    img = e.Image.open(f'images/{e.randint(1, 10)}.png')  # opening an image from the source path
    # img = Image.open(f'images/{10}.png')
    result = e.pytesseract.image_to_string(img, lang='por')  # converts image to result and saves it into result variable
    """language = langdetect.detect(result)
    if language == "en":
        result = pytesseract.image_to_string(img)  # does the conversion again but taking it as english"""
    print(result)
