from loading_images import *
from recognition import *
from modification import *
from animation import *
import os


test_list = []
path = r"C:\Users\Rob\Documents\GitHub\hdp-images\hdp-images\recognized_faces"
for file in os.listdir(path):
    test_list.append(f"{path}\\{file}")

load_jpg(test_list)