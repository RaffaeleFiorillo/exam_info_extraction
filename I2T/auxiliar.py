import os

exercises_directory = "C:/Users/rfior/OneDrive/Desktop/PFC/DB/Exercises"

def rename_files_numerically(directory, start_point=1):
    for i, image in enumerate(list(os.walk(directory))[0][2]):
        if len(image) > 10:
            os.rename(f"{directory}/{image}", f"{directory}/{start_point+i}.jpg")


rename_files_numerically(exercises_directory, 74)

