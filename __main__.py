from modem import Modem
from ser import Ser
from _file import Utils
import constant
import time
from multiprocessing.dummy import Pool as ThreadPool
import argparse
import sys
from functools import partial


def sms_function(sms_text, phone, port):
    ser = Ser(port)
    # ser.delete_sms()
    time.sleep(2)
    ser.send_sms(sms_text, phone)
    phone_number = ser.get_phone_number("*101#")[0]
    return (port, phone_number, ser.read_sms())
    

"""
    Check argument to use function
"""

def execute_options():
    parser = argparse.ArgumentParser(description="""This is SMS Modem Python""")
    parser.add_argument('-s','--sms', nargs=2, help='Send sms <With text> to <Phone_number>', metavar=('SMS_Text', 'Phone_Number'))
    parser.add_argument('-c','--call', nargs=1, help='Calling number xxx', metavar='Phone_Number')
    args = parser.parse_args()

    if args.sms is not None:
        modem = Modem()
        devices = modem.devices
       
        pool = ThreadPool(16)
        f = partial(sms_function, *args.sms)
        result = pool.map(f, devices)
        
        # # close the pool and wait for the work to finish 
        pool.close() 
        pool.join()
        _file = Utils(constant.SMS_FILE)
        for iterator in result:
            (port, phone_number, sms) = iterator
            try:
                _file.write_sms_to_file(port, phone_number.decode(), sms)
            except:
                print('No number')

    elif args.call is not None:
        modem = Modem()
        devices = modem.devices
        for iterator in devices:
            ser = Ser(iterator)
            ser.call(*args.call)
    else:
        sys.exit(2)

if __name__ == "__main__":
    execute_options()