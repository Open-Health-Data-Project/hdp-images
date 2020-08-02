# Team 4
import face_recognition
import cv2
import exifread
from loading_images import *


class Face:
    possible_composition = "straight", "left-side", "right-side", "portrait", None

    def __init__(self, photo, date_taken, dir, composition=None, face=None, avg_height=0, avg_width=0):
        self.photo = photo
        self.date_taken = date_taken
        self.dir = dir
        self.composition = composition if composition in Face.possible_composition else None
        self.face = face
        self.avg_height = avg_height
        self.avg_width = avg_width


def recognize_face(loaded_faces_list):
    for loaded_face in loaded_faces_list:

        # Load the image into a Python Image Library object so that we can draw on top of it and display it
        image_marked = loaded_face.photo.copy()
        directory = "recognized_faces\\"
        recognized_faces = []

        # Load the jpg file into a numpy array
        image = loaded_face.photo

        # Find all the faces in the image
        face_locations = face_recognition.face_locations(image)

        number_of_faces = len(face_locations)
        print("I found {} face(s) in this photograph.".format(number_of_faces))

        counter = 1
        for face_location in face_locations:
            # Print the location of each face in this image. Each face is a list of co-ordinates in (top, right, bottom,
            # left) order.
            top, right, bottom, left = face_location
            # print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left,
            # bottom, right))

            # Let's draw a box around the face
            margin = (bottom - top) // 2
            window_name = "Znalezione"
            top = top - margin - (margin // 2)
            left = left - margin
            bottom = bottom + margin
            right = right + margin
            start_point = (left, top)
            end_point = (right, bottom)
            color = (0, 0, 255)
            thickness = 2
            image_marked = cv2.rectangle(image_marked, start_point, end_point, color, thickness)

            crop_img = loaded_face.photo[top:bottom, left:right].copy()
            dir = directory + str(counter) + ".jpg"
            cv2.imwrite(dir, crop_img)
            loaded_face.face = crop_img
            #recognized_faces.append(Face(crop_img, dateTaken, dir))
            counter += 1

        # Display the image on screen
            #cv2.imshow(window_name, image_marked)
            #cv2.waitKey()

    return loaded_faces_list


#list_of_faces = recognize_face("people.jpg")

#for item in list_of_faces:
 #   print(item.dir)
