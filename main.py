import argparse
import os
from Auxiliar import auxiliary
from Segmentation import segmentation as segment
from I2T import extraction


ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", type=str, help="path to exam/test image(s). Could be a folder")
ap.add_argument("-sd", "--save_dir", type=str, default="Results", help="path where the extracted text will be saved")
# ap.add_argument("-t", "--test", default=True, type=bool, help="run the code in the test script")
# ap.add_argument("-", "--", type=, default=, help="")
args = vars(ap.parse_args())

if __name__ == "__main__":
    if os.path.isfile(args["image"]):  # extract information from an image
        coo = segment.get_segmented_directory([args["image"]])[0]
        print(args["image"])
        exam = extraction.Exam(args["image"], coo)
        exam.extract_information(args["save_dir"])
    elif os.path.isdir(args["image"]):  # extract information from a group of images within a folder
        sub_directories = auxiliary.get_sub_directories(args["image"])
        coo = segment.get_segmented_directory(sub_directories)
        for c, d in zip(coo, sub_directories):
            exam = extraction.Exam(d, c)
            exam.extract_information(args["save_dir"])
    else:  # path does not exist
        exit(f"Error: Image/folder: {args['image']} does not exist")
