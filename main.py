from modem import Modem
from ser import Ser
from _file import Utils
import constant
import time
from multiprocessing.dummy import Pool as ThreadPool
import argparse

def function(port):
    ser = Ser(port)

    ser.delete_sms()
    time.sleep(2)
    ser.send_sms('GC', '195')
    phone_number = ser.get_phone_number("*101#")[0]
    return (port, phone_number.decode(), ser.read_sms())
    

"""
    Check argument to use function
"""
if __name__ == "__main__":
    modem = Modem()
    _file = Utils(constant.SMS_FILE)
    devices = modem.devices
    pool = ThreadPool(16) 
    results = pool.map(function, devices)
    print('pool result', results)
    
    # close the pool and wait for the work to finish 
    pool.close() 
    pool.join()
    _file = Utils(constant.SMS_FILE)
    for iterator in results:
        (port, phone_number, sms) = iterator
        try:
            _file.write_sms_to_file(port, phone_number, sms)
        except:
            print('No number')
    # parser = argparse.ArgumentParser()

    # parser.add_argument('-c', action='store', dest='calling number', help='Calling number xxx')
    # results = parser.parse_args()
    # print('simple_value     =', results.simple_value)