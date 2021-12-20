import can
import logging
import os
import asyncio
import time
logger = logging.getLogger(__name__)

class CanHandler:
    def __init__(self, demo=False):
        self.instance = object
        self.notifier = object
        self.demo =demo
        self.status_ok = {'status': 'ok'}
        self.read_continue = True

    def open_instr(self, bitrate=500000):
        if not self.demo:
            try:
                os.system(f'sudo ip link set can0 type can bitrate {bitrate}')
                os.system('sudo ifconfig can0 up')
                self.instance = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=bitrate)
                logger.debug(f'CAN:bus opened in can0 with bitrata:{bitrate}')
                return self.status_ok
            except can.CanError as e:
                raise IOError(e)
        else:
            return self.status_ok

    def close_instr(self):
        if not self.demo:
            try:
                self.notifier.stop()
                self.instance.shutdown()
                # self.instance=None
                os.system('sudo ifconfig can0 down')
                logger.debug('CAN:can bus on can0 is closed!')
                return self.status_ok
            except can.CanError as e:
                raise IOError(e)
        else:
            return self.status_ok

    def msg_payload(self, id, data, isExtId):
        if not self.demo:
            try:
                # data_hex = list(hex(i) for i in data)
                # id_hex = hex(id)
                return can.Message(arbitration_id=id, data=data,is_extended_id=isExtId)
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok

    def send_msg(self, id=0xc0ffee, data=[0,25,0,1,3,1,4,1], isExtId=True, timeout=0.0001):
        if not self.demo:
            try:
                self.instance.send(self.msg_payload(id=id,data=data,isExtId=isExtId), timeout=timeout)
                # logger.debug(f'CAN: send msg : {id, data}')
                return self.status_ok
            except can.CanError as e:
                raise IOError(e)
        else:
            return self.status_ok
    
    def recv_msg(self, timeout):
        """timeout 1.0, 2.0  in seconds"""
        if not self.demo:
            try:
                resp = self.instance.recv(timeout)
                logger.debug(f'CAN: recv msg: {resp}')
                return resp
            except can.CanError as e:
                raise IOError(e)
        else:
            return 0

    async def receive_notify(self,loop):
        reader = can.AsyncBufferedReader()
        logger = can.Logger('logfile.asc')
        listeners = [reader,logger]
        # loop = asyncio.get_event_loop()
        self.notifier = can.Notifier(self.instance, listeners, loop=loop)
        resp = await reader.get_message()
        return resp

# if __name__ == '__main__':
#     handl = CanHandler()
#     handl.open_instr()
#     handl.send_msg()
#     handl.close_instr()
