import serial
import re
import serial.tools.list_ports
from natsort import natsorted

class Modem: 
	devices = []
	port = None
	ser = None


	def __init__(self):
		self.devices = self._get_all_ports()
		self.port = self._get_number_ports()
	"""
		Chunks list to n
	"""
	def divide_chunks(self, l, n):
		for i in range(0, len(l), n):  
			yield l[i:i + n]
	"""
		Filter ports COM
	"""
	def _get_all_ports(self):
		ports = serial.tools.list_ports.comports()
		description = [port.description for port in ports]
		regex = re.compile(r'^XR21V1414 USB UART Ch ')
		filter_COM = sorted(list(filter(regex.search, description)))
		
		for i in filter_COM:
			group = re.match(r'^XR21V1414 USB UART Ch .* \((COM.*)\)', i).group(1)
			self.devices.append(group)
		chunks = list(self.divide_chunks(self.devices, 4))
		sort_chunks = [natsorted(iterator) for iterator in chunks]
		new_sort = []
		for i in range(0, len(sort_chunks)):
			for j in range(0, len(sort_chunks[i])):
				new_sort.append(sort_chunks[j][i])
		self.devices = new_sort
		print('devices: ', self.devices)
		return self.devices
		
	def _get_number_ports(self):
		print("Number port: ", len(self.devices))
		return len(self.devices)

	def get_port(self, port):
		self.port = port
		print("Get port: ", self.port)
		return self.port

