# Team 4
import cv2
import glob
import uuid
from modification import *


# e.g. frames_per_seconds = 2 means 2 images per 1 second
def create_animation(loaded_faces_list: list, frames_per_second=10):
    # Creating the unique animation title.
    animation_title = str(uuid.uuid4()) + ".mp4"
    animation_size = (loaded_faces_list[0].face.shape[1], loaded_faces_list[0].face.shape[0])

    # Creating list for images at a given face_composition.
    image_array = []
    for loaded_face in loaded_faces_list:
        image_array.append(loaded_face.face)

    animation = cv2.VideoWriter(animation_title, cv2.VideoWriter_fourcc(*"mp4v"), frames_per_second, animation_size)

    for image in image_array:
        # write() includes only the images that have the same size as has been specified when opening the video writer
        animation.write(image)

    animation.release()

    return animation

