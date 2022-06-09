# ------------------------------------------ SEGMENTATION --------------------------------------------------------------
# directory of the segmentation model
seg_model_dir = "Segmentation/mask_rcnn_models/mask_rcnn_model_v1.h5"
class_names = ["BG", "enunciado"]  # names of the classes used to train the segmentation model
class_number = len(class_names) - 1  # number of classes the model is able to distinguish. "BG" is not considered

# ----------------------------------------- IMAGE TO TEXT --------------------------------------------------------------
tesseract_path = "Tesseract-OCR/tesseract.exe"
