from loading_images import *
from recognition import *
from modification import *
from animation import *
import os


test_list = []
path = r"/Users/rob/Documents/GitHub/hdp-images/hdp-images/recognized_faces"
for file in os.listdir(path):
    test_list.append(f"{path}/{file}")
loaded = load_jpg(test_list)
recognized = recognize_face(loaded)
face_aligned = face_align(recognized)
create_animation(face_aligned)