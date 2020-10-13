from loading_images import *
from recognition import *
from modification import *
from animation import *
import os
import pathlib

test_list = []
path = pathlib.Path(r"")
for file in os.listdir(path):
    test_list.append(path.joinpath(file))
    if len(test_list) > 10:
        break
loaded = load_jpg(test_list)
# recognized = recognize_face(loaded)
for image in loaded:
    image.face = image.photo
face_aligned = face_align(loaded)
create_animation(face_aligned)
