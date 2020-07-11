import exifread
import os
from datetime import datetime, date
import re


class JpgLoader:
	def __init__(self, file, argument):
		self.argument = argument
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

	def check_name_for_date(self):
		if self.fulfilled is not True:
			try:
				name = self.file.name
				match = re.search(r'\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}', name)
				self.date = datetime.strptime(match.group(), '%Y%m%d_%H%M%S')
				self.fulfilled = True
				print('Date from name')
				return self
			except AttributeError:
				return self
		return self

	def insert_argument(self):
		if self.fulfilled is not True:
			try:
				name = self.argument
				match = re.search(r'\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}', name)
				self.date = datetime.strptime(match.group(), '%Y%m%d_%H%M%S')
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


def load_jpg(images_paths: list):
	list_of_faces = []
	for image in images_paths:
		file_path = image
		with open(file_path, 'rb') as f:
			loader = JpgLoader(f, "tutaj argument do regular expr")
			date_taken = loader.check_exif().check_name_for_date().insert_argument().check_date_of_creation().get_date()

			#bedziemy tworzyc nowy obiekt z klasy Face(photo, date_taken, dir, composition)
			#new_face = Face(image, date_taken, f)
			#list_of_faces.append(new_face)

			#print to test if works then delete
			print(date_taken)


#test function
load_jpg(['path1', 'path2', 'etc...'])

