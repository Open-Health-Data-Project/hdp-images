import exifread
import os
from datetime import datetime
from recognition import *
from clean import *


class JpgLoader:
	def __init__(self, file, argument, date_format):
		self.argument = argument
		self.date_format = date_format
		self.file = file
		self.fulfilled = False
		self.date = ""

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
				self.date = convert_date(self.argument, self.date_format, mode='regex')
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


def load_jpg(images_paths: list, mode='all'):
	loaded_faces = []
	for image in images_paths:
		file_path = image
		with open(file_path, 'rb') as f:
			loader = JpgLoader(f, 'regex', date_format='string')
			date_taken = loader.check_exif().insert_argument().check_date_of_creation().get_date()
			face = Face(image, date_taken, f)
			loaded_faces.append(face)
	return loaded_faces
