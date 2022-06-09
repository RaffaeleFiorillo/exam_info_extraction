import os
from pixellib.custom_train import instance_custom_training


def rename_all(name, dir_files):
    os.chdir(dir_files)
    print(os.getcwd())

    for count, f in enumerate(os.listdir()):
        f_name, f_ext = os.path.splitext(f)
        f_name = f"{name} ({count + 1})"

        new_name = f'{f_name}{f_ext}'
        # print(new_name)
        os.rename(f, new_name)

def rename_database():
    rename_all("enunciado", "C:/Users/rfior/OneDrive/Documents/butterfly/Exams/test/xml")
    rename_all("enunciado", "C:/Users/rfior/OneDrive/Documents/butterfly/Exams/test/img")
    rename_all("enunciado", "C:/Users/rfior/OneDrive/Documents/butterfly/Exams/train/img")
    rename_all("enunciado", "C:/Users/rfior/OneDrive/Documents/butterfly/Exams/train/xml")

def visualize_dataset():
    vis_img = instance_custom_training()
    vis_img.load_dataset("Exams")
    vis_img.visualize_sample()

def get_sub_directories(folder_dir):
    return [f"{folder_dir}\\{name}" for name in os.listdir(folder_dir) if os.path.isfile(os.path.join(folder_dir, name))]
