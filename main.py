from dataclasses import dataclass
from abc import ABC, abstractmethod

class baseField(ABC):
	def __init__(self):
		self._width = 10
		self._height = 20
		self._field = {}

	def createField(self):
		field = []
		for y in range(self._height):
			line = []
			for x in range(self._width):
				line.append('0')
			field.append(line)
		print(field)

# @dataclass(frozen=True)
class playField():
	def __init__(self):
		pass

	def moveDown(self):
		pass
