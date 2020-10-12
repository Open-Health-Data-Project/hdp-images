from facealigner_modified import FaceAligner
from imutils.face_utils import rect_to_bb
import dlib
from recognition import *
from face_cut import *


def check_avg_size(loaded_faces_list: list):
    width_sum = 0
    height_sum = 0
    for loaded_face in loaded_faces_list:
        height, width, _ = loaded_face.face.shape
        width_sum += width
        height_sum += height
    width_avg = width_sum // len(loaded_faces_list)
    height_avg = height_sum // len(loaded_faces_list)
    return height_avg, width_avg


def face_align(loaded_faces_list: list):
    height_avg, width_avg = check_avg_size(loaded_faces_list)
    predictor = dlib.shape_predictor(r"shape_predictor_68_face_landmarks.dat")
    fa = FaceAligner(predictor, desiredFaceWidth=int(width_avg), desiredFaceHeight=height_avg, desiredLeftEye=(0.3, 0.5))
    # load the input image, resize it, and convert it to grayscale
    for loaded_face in loaded_faces_list:
        image = loaded_face.face
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detector = dlib.get_frontal_face_detector()
        rects = detector(gray, 2)
        print("Processing...")

        # loop over the face detections
        for rect in rects:
            # extract the ROI of the *original* face, then align the face
            # using facial landmarks
            (x, y, w, h) = rect_to_bb(rect)
            face_aligned, params = fa.align(image, gray, rect)
            loaded_face.avg_width = face_aligned.shape[1]
            loaded_face.avg_height = face_aligned.shape[0]
            loaded_face.face = face_aligned
            cv2.imshow("Aligned", face_aligned)
            cv2.waitKey()
            largest_rect = largest_rotated_rect(params[0], params[1], params[2])
            face_aligned_cropped = crop_around_center(face_aligned, *largest_rect)
            cv2.imshow("Cropped", face_aligned_cropped)
            cv2.waitKey()

        # display the output images
        # cv2.imshow("Original", loaded_face.photo)
        # cv2.imshow("Aligned", face_aligned)
        # cv2.waitKey(0)
    return loaded_faces_list
