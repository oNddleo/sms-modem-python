import serial
import re
import serial.tools.list_ports


class Modem: 
	devices = []
	port = None
	ser = None


	def __init__(self):
		self._get_all_ports()
		self._get_number_ports()
	"""
		Filter ports COM
	"""
	def _get_all_ports(self):
		ports = serial.tools.list_ports.comports()
		description = [port.description for port in ports]
		regex = re.compile(r'^XR21V1414 USB UART Ch ')
		filter_COM = list(filter(regex.search, description))

		for i in filter_COM:
			group = re.match(r'^XR21V1414 USB UART Ch .* \((COM.*)\)', i).group(1)
			self.devices.append(group)
		print("Devices: ", self.devices)
		return self.devices
		
	def _get_number_ports(self):
		print("Number port: ", len(self.devices))
		return len(self.devices)

	def get_port(self, port):
		self.port = port
		print("Get port: ", self.port)
		return self.port

