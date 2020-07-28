from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import argparse
import imutils
import dlib
import cv2


def aligner(shape_predictor: str):
	predictor = dlib.shape_predictor(shape_predictor)
	# trzeba sie zastanowic nad desirefacewidth rozdzielczosc zdj
	fa = FaceAligner(predictor, desiredFaceWidth=256)
	return fa


def face_align(image_path: str, fa, dir_img: str):
	# load the input image, resize it, and convert it to grayscale
	image = cv2.imread(image_path)
	image = imutils.resize(image, width=800)
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
		cv2.imwrite(f"{dir_img}.jpg", face_aligned)

		# display the output images
		# cv2.imshow("Original", faceOrig)
		# cv2.imshow("Aligned", faceAligned)
		# cv2.waitKey(0)


face_align("/Users/rob/Documents/GitHub/hdp-images/hdp-images/recognized_faces/3.jpg",
		   aligner("/Users/rob/Documents/GitHub/hdp-images/hdp-images/shape_predictor_68_face_landmarks.dat"),
		   "aligned")