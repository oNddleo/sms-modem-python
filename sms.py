import serial
import json
import time
import serial.tools.list_ports
# import gsmself.ser.pdu
import re

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
		self.ser = serial.Serial(port, baudrate=9800, timeout=1)
		return self.port

	def get_phone_number(self, ussd):
		print("GET NUMBER")
		self.ser.write(b'AT+CUSD=1, "%s"\r\n' % ussd.encode())
		time.sleep(10)
		ret = self.filter_message()
		remove_ok = list(filter(lambda e : e != b'OK', ret))
		result = []
		cusd = b''
		# Get number get, balance and expriry date
		for i in remove_ok:
			if i.startswith(b'+CUSD: ') == True and cusd != b'' or i == remove_ok[-1]:
				result.append(cusd)
				cusd = b''
			cusd = b''.join([cusd, i])
		# Regex get number
		number = None
		balance = None
		expried_date = None
		for i in result:
			if(i != b''):
				regex = re.compile(b'.*"(\d+). TKG: (\d+)d.*0h ngay (\d+/\d+/\d+).')
				number = regex.match(i).group(1)
				balance = regex.match(i).group(2)
				expried_date = regex.match(i).group(3)
				print(b'number: %s , balance: %s, expried_date: %s' % (number, balance, expried_date))
		self.ser.write(b'AT+CUSD=2\r\n')
		return (number, balance, expried_date)
	def send_sms(self, message, phonenumber):
		self.ser.write(b'AT+CMGF=1\r')
		# send sms
		print("Sending sms to: %s with message: %s" % (phonenumber, message))
		self.ser.write(b'AT+CMGS="' + phonenumber.encode() + b'"\r')
		time.sleep(0.5)
		self.ser.write(message.encode() + b"\r")
		time.sleep(0.5)
		self.ser.write(b'\x1A\r\n')
		time.sleep(0.5)
		response = self.ser.readlines()
		time.sleep(0.5)
		print("SENT")

	"""
		Filter \r\n in msg 
	"""
	def filter_message(self):
		ret = []
		while self.ser.inWaiting() > 0:
			msg = self.ser.readline().strip()
			# print('message: ', msg)
			msg = msg.replace(b'\r',b'')
			msg = msg.replace(b'\n',b'')
			if msg != b'':
				ret.append(msg)
		return ret

	"""
		Calling Service 
		Calling number and set timeout when accept
		
	"""
	def call(phone_number, timeout):
		
		print("CALLING PHONE")
		ser.write(b'ATD0915834454;\r\n')

	"""
		SMS Service
		Read all messages
	"""
	def read_sms(self):
		print("LOOKING FOR SMS")
		# pdu = "07914889200026F5040B914819854354F400009170226170428208F3F61C442FCFE9"
		# sms = gsmself.ser.pdu.decodeSmsPdu(pdu)
		# print(json.dumps(sms))

		self.ser.write(b'AT+CMGF=1\r\n')
		time.sleep(0.5)
		
		self.ser.write(b'AT+CMGL="ALL"\r\n')
		time.sleep(1)
		# filter sms \r\n and strip
		filter_sms = self.filter_message()
		filter_oke = list(filter(lambda e : e != b'OK', filter_sms))

		result = []
		sms_done = b''
		if(len(filter_oke) > 0):
			first = filter_oke[0]
			sms_done = first
			iterator = 1
			while iterator <= len(filter_oke) - 1:
				if filter_oke[iterator].startswith(b'+CMGL:') == True and sms_done != b'':
					result.append(sms_done)
					first = filter_oke[iterator]
					sms_done = first
				else:
					first = b''
					sms_done = sms_done + b',"' + filter_oke[iterator] + b'"'
				if iterator == len(filter_oke) - 1:
					result.append(sms_done)
					break
				iterator += 1

			print('result: ', result)
		return result