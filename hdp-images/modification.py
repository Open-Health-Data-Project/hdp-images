from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import dlib
from recognition import *
from face_cut import *
import time


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
    fa = FaceAligner(predictor, desiredFaceWidth=int(0.85 * width_avg),
                     desiredFaceHeight=height_avg, desiredLeftEye=(0.3, 0.5))
    # load the input image, resize it, and convert it to grayscale
    global_optimum_crop = [0, 0, 0, 0]
    for photo_nr, loaded_face in enumerate(loaded_faces_list, 1):
        start_time = time.time()
        image = loaded_face.face
        # image = cv2.normalize(image, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC3)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detector = dlib.get_frontal_face_detector()
        rects = detector(gray, 2)
        # loop over the face detections
        for rect in rects:
            # extract the ROI of the *original* face, then align the face
            # using facial landmarks
            (x, y, w, h) = rect_to_bb(rect)
            face_aligned = fa.align(image, gray, rect)
            face_aligned = crop(face_aligned)
            shape = (face_aligned.shape[1], face_aligned.shape[0])
            loaded_face.face = face_aligned
            current_crop = find_optimal_crop(face_aligned, shape[0], shape[1])
            global_optimum_crop = [max(e1, e2) for e1, e2 in zip(global_optimum_crop, current_crop)]
        stop_time = time.time()
        print("Alignment of photo nr", photo_nr, "takes {:.2f} s.".format(stop_time - start_time))
        # cv2.imshow("Aligned", face_aligned)
        # cv2.waitKey()
    h1, h2, w1, w2 = global_optimum_crop
    for loaded_face in loaded_faces_list:
        loaded_face.face = loaded_face.face[h1:h2, w1:w2]
    print(f"Final photos shape {loaded_faces_list[0].face.shape[0]} x {loaded_faces_list[0].face.shape[1]}.")
    return loaded_faces_list
