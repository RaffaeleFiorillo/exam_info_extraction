from pixellib.instance import custom_segmentation
import Auxiliar.config as conf


def get_segmented_directory(img_directories):
    tests = []  # all tests will be here. Each test is a group (list) of the coordinates for each of his exercises
    segment_image = custom_segmentation()
    segment_image.inferConfig(num_classes=conf.class_number, class_names=conf.class_names)
    segment_image.load_model(conf.seg_model_dir)
    for directory in img_directories:
        # coordinates for each exercise's bounding box
        co = segment_image.segmentImage(directory, show_bboxes=True)  # , output_image_name=f"sample_out{i}.jpg")
        tests.append(list(co[0]['rois']))  # alter here for more classes to be extracted and saved
    return tests


