from loading_images import *
from recognition import *
from modification import *
from animation import *
import os


test_list = []
path = r""
for file in os.listdir(path):
    test_list.append(fr"{path}\{file}")
    if(len(test_list) > 10):
        break
loaded = load_jpg(test_list)
recognized = recognize_face(loaded)
face_aligned = face_align(recognized)
create_animation(face_aligned)
