import exifread
import os
from datetime import datetime
import re
import pandas as pd


def convert_date(date: str, date_format: str = None, mode: str = 'flag'):
	possible_keys = {'year', 'month', 'day', 'hour', 'minute', 'second', 'time_zone'}
	if mode == 'regex':
		if re_compiler(date_format) is True:
			try:
				date_dict = re.search(date_format, date).groupdict()
				date_dict = dict_comprehension(possible_keys, date_dict)
				return pd.Timestamp(**date_dict)
			except AttributeError:
				return str(date)
		else:
			return str(date)


def re_compiler(format: str) -> bool:
	try:
		re.compile(format)
		return True

	except re.error:
		return False


def get_month_number(value: str) -> int:
	"""

	Parameters
	----------
	value: string containing short or full month name - min 3 chars long

	Returns
	-------
	int representing month number
	"""
	return {'jan': 1,
			'feb': 2,
			'mar': 3,
			'apr': 4,
			'may': 5,
			'jun': 6,
			'jul': 7,
			'aug': 8,
			'sep': 9,
			'oct': 10,
			'nov': 11,
			'dec': 12
			}[value[:3].lower()]


def dict_comprehension(possible_keys: set, initial_dict: dict) -> dict:
	for k, v in initial_dict.copy().items():
		try:
			initial_dict[k] = int(v)
		except ValueError:
			initial_dict[k] = get_month_number(v)
	new_dict = {k if k in possible_keys else None: 0 if v == '' else int(v) for k, v in initial_dict.items()}
	if None in new_dict.keys():
		raise KeyError
	return new_dict


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
				# jezeli bedize string to lecimy dalej
				if type(self.date) == str:
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
	list_of_faces = []
	for image in images_paths:
		file_path = image
		with open(file_path, 'rb') as f:
			loader = JpgLoader(f, '20002020202020', date_format='string')
			date_taken = loader.check_exif().insert_argument().check_date_of_creation().get_date()

			#bedziemy tworzyc nowy obiekt z klasy Face(photo, date_taken, dir, composition)
			#new_face = Face(image, date_taken, f)
			#list_of_faces.append(new_face)

			#print to test if works then delete
			print(date_taken)


#test function
load_jpg(['C:/Users\Rob\Documents\GitHub\hdp-images\hdp-images\people.jpg'])

