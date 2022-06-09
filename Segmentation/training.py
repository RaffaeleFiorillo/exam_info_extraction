import pixellib
from pixellib.custom_train import instance_custom_training


def train_dataset():
    train_maskrcnn = instance_custom_training()
    train_maskrcnn.modelConfig(network_backbone="resnet101", num_classes=1, batch_size=4)
    train_maskrcnn.load_pretrained_model("mask_rcnn_coco.h5")
    train_maskrcnn.load_dataset("Exams")
    train_maskrcnn.train_model(num_epochs=300, augmentation=True, path_trained_models="mask_rcnn_models")


def evaluate_model():
    train_maskrcnn = instance_custom_training()
    train_maskrcnn.modelConfig(network_backbone="resnet101", num_classes=1)
    train_maskrcnn.load_dataset("Exams")
    train_maskrcnn.evaluate_model("mask_rcnn_model_30.h5")

