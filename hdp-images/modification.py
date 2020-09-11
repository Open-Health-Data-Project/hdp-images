from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import imutils
import dlib
import cv2
from recognition import *


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
	# trzeba sie zastanowic nad desirefacewidth rozdzielczosc zdj
	fa = FaceAligner(predictor, desiredFaceWidth=int(0.9*width_avg), desiredFaceHeight=int(0.9*height_avg))
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
			#faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
			face_aligned = fa.align(image, gray, rect)
			face_aligned = imutils.resize(face_aligned, height=height_avg, width=width_avg)
			loaded_face.avg_width = width_avg
			loaded_face.avg_height = height_avg
			loaded_face.face = face_aligned

			# display the output images
			# cv2.imshow("Original", faceOrig)
			# cv2.imshow("Aligned", faceAligned)
			# cv2.waitKey(0)
	return loaded_faces_list
