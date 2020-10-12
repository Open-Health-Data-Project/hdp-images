import exifread
import os
from datetime import datetime
from recognition import Face
from clean import convert_date
import pathlib
import cv2


class JpgLoader:
	def __init__(self, file, file_name, date_format, mode, composition):
		self.file_name = file_name
		self.date_format = date_format
		self.file = file
		self.fulfilled = False
		self.date = ""
		self.mode = mode
		self.composition = composition

	def check_exif(self):
		try:
			tags = exifread.process_file(self.file, stop_tag="EXIF DateTimeOriginal")
			self.date = tags["EXIF DateTimeOriginal"]
			self.fulfilled = True
			print('EXIF')
			return self
		except KeyError:
			return self

	def insert_argument(self):
		if self.fulfilled is not True:
			try:
				self.date = convert_date(self.file_name, self.date_format, mode=self.mode)
				if type(self.date) == str:
					return self
				self.fulfilled = True
				print('Date from regex')
				return self
			except AttributeError:
				return self
		return self

	def check_date_of_creation(self):
		if self.fulfilled is not True:
			date_of_creation = os.stat(self.file.name).st_ctime
			self.date = datetime.fromtimestamp(date_of_creation)
			self.date = self.date.strftime("%Y-%m-%d %H:%M:%S")
			self.fulfilled = True
			print('Date from creation')
			return self
		return self

	def get_date(self):
		return self.date


def load_jpg(images_paths: list, mode='regex', date_format: str = "", composition="portrait"):
	loaded_faces_list = []
	for image in images_paths:
		file_path = pathlib.Path(image)
		with open(file_path, 'rb') as f:
			loader = JpgLoader(f, file_path.name, date_format, mode, composition)
			date_taken = loader.check_exif().insert_argument().check_date_of_creation().get_date()
			loaded_face = cv2.imread(image)
			face_shape = loaded_face.shape
			if face_shape[0]*face_shape[1] > 2000000:
				factor = 2000000 / (face_shape[0]*face_shape[1])
				resized_face = cv2.resize(loaded_face, (int(face_shape[1]*factor), int(face_shape[0]*factor)))
				print(resized_face.shape)
			else:
				resized_face = loaded_face
			new_face = Face(resized_face, date_taken, f)
			loaded_faces_list.append(new_face)
	return loaded_faces_list
