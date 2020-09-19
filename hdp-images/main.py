from loading_images import *
from recognition import *
from modification import *
from animation import *
import os


test_list = []
path = r"C:\Users\adama\OneDrive\Obrazy\face"
for file in os.listdir(path):
    test_list.append(fr"{path}\{file}")
loaded = load_jpg(test_list)
# recognized = recognize_face(loaded)
for image in loaded:
    image.face = image.photo
face_aligned = face_align(loaded)
create_animation(face_aligned)
