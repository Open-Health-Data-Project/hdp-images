from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import imutils
import dlib
import cv2
from recognition import *


def check_avg_width(loaded_faces_list: list):
	width_sum = 0
	for loaded_face in loaded_faces_list:
		_, width, _ = loaded_face.face.shape
		width_sum += width
	width_avg = width_sum // len(loaded_faces_list)
	return width_avg


def face_align(loaded_faces_list: list):
	width_avg = check_avg_width(loaded_faces_list)
	predictor = dlib.shape_predictor("/Users/rob/Documents/GitHub/hdp-images/hdp-images/shape_predictor_68_face_landmarks.dat")
	# trzeba sie zastanowic nad desirefacewidth rozdzielczosc zdj
	fa = FaceAligner(predictor, desiredFaceWidth=int(0.9*width_avg))
	# load the input image, resize it, and convert it to grayscale
	width_avg = check_avg_width(loaded_faces_list)
	for loaded_face in loaded_faces_list:
		image = imutils.resize(loaded_face.face, width=width_avg)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		detector = dlib.get_frontal_face_detector()
		rects = detector(gray, 2)

		# loop over the face detections
		for rect in rects:
			# extract the ROI of the *original* face, then align the face
			# using facial landmarks
			(x, y, w, h) = rect_to_bb(rect)
			#faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
			face_aligned = fa.align(image, gray, rect)
			loaded_face.avg_width = w
			loaded_face.avg_height = h
			loaded_face.face = face_aligned

			# display the output images
			# cv2.imshow("Original", faceOrig)
			# cv2.imshow("Aligned", faceAligned)
			# cv2.waitKey(0)
	return loaded_faces_list

#face_align("/Users/rob/Documents/GitHub/hdp-images/hdp-images/recognized_faces/3.jpg",
#		   aligner("/Users/rob/Documents/GitHub/hdp-images/hdp-images/shape_predictor_68_face_landmarks.dat"),
#		   "aligned", check_avg_width(loaded_faces_list=))