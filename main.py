from sms import Modem
from _file import Utils
import constant
import time
from multiprocessing.dummy import Pool as ThreadPool


def function(device):
    _port = sms.get_port(device)
    _phone_number = sms.get_phone_number("*101#")[0]
    print('phone number', _phone_number)
    try:
        _file.write_sms_to_file(_port, _phone_number.decode(), sms.read_sms())
    except:
        print('No number')
if __name__ == "__main__":
    sms = Modem()
    # pool = ThreadPool(16) 
    # print('pool', pool)
    # results = pool.map(function, sms.devices)

    # close the pool and wait for the work to finish 
    # pool.close() 
    # pool.join()
    _file = Utils(constant.SMS_FILE)
    # for s in sms.devices:
    #     _port = sms.get_port(s)
    #     sms.send_sms('GC', '195')

    for s in sms.devices:
        _port = sms.get_port(s)
        _phone_number = sms.get_phone_number("*101#")[0]
        print('phone number', _phone_number)
        try:
            _file.write_sms_to_file(_port, _phone_number.decode(), sms.read_sms())
        except:
            print('No number')
