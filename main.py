from sms import Modem
from ser import Ser
from _file import Utils
import constant
import time
from multiprocessing.dummy import Pool as ThreadPool


def function(port):
    ser = Ser(port)
    ser.send_sms('GC', '195')
    phone_number = ser.get_phone_number("*101#")[0]
    _file = Utils(constant.SMS_FILE)
    try:
        _file.write_sms_to_file(port, phone_number.decode(), ser.read_sms())
    except:
        print('No number')

if __name__ == "__main__":
    sms = Modem()
    _file = Utils(constant.SMS_FILE)
    devices = sms.devices
    pool = ThreadPool(16) 
    results = pool.map(function, devices)

    # close the pool and wait for the work to finish 
    pool.close() 
    pool.join()
