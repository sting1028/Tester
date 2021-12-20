import logging
import RPi.GPIO as GPIO
import serial
logger = logging.getLogger(__name__)

class SerialHandler:
    def __init__(self, demo=False, gpio=None, interface=''):
        self.instance = None
        self.demo =demo
        self.status_ok = {'status': 'ok'}
        self.gpio = gpio
        self.mode = None
        self.interface = interface

    def open_instr(self, bitrate=115200, mode='ttl',bytesize=8,parity='none',stopbit=1):
        """bytesize: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS"""
        """parity: PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE"""
        self.mode = mode
        byte_size_table = {5: serial.FIVEBITS,
                            6: serial.SIXBITS,
                            7: serial.SEVENBITS,
                            8: serial.EIGHTBITS}
        parity_table = {
            'none': serial.PARITY_NONE,
            'even': serial.PARITY_EVEN,
            'mark':serial.PARITY_MARK,
            'odd':serial.PARITY_ODD,
            'space':serial.PARITY_SPACE
        }
        stop_bit_table = {
            1: serial.STOPBITS_ONE,
            2: serial.STOPBITS_TWO,
        }
        if not self.demo:
            try:
                # if mode in ('485-auto', '485-manual', 'ttl'):
                #     interface = "/dev/ttyS0"
                # elif mode == 'usb':
                #     interface = "/dev/ttyACM0"
                # else:
                #     raise ValueError('only support 485-auto, 485-manual, ttl, usb')
                self.instance = serial.Serial(port=self.interface,baudrate=bitrate,timeout=5,bytesize=byte_size_table[bytesize],parity=parity_table[parity],stopbits=stop_bit_table[stopbit])
                if not self.instance.is_open:
                    self.instance.open()
                logger.debug('Serial: bus opened!')
                return self.status_ok
            except Exception as e:
                raise ValueError(e)
        else:
            return self.status_ok
    
    def close_instr(self):
        if not self.demo:
            try:
                self.instance.close()
                self.instance = None
                logger.debug('Serial: bus closed!')
                return self.status_ok
            except Exception as e:
                raise ValueError(e)
        else:
            return self.status_ok

    def mode_select(self,rw):
        #only for half-auto, EN_485 = LOW is Receiver, EN_485 = HIGH is Send
        if not self.demo:
            try:
                EN_485 =  7
                self.gpio.setup_channel_out(pin=[EN_485],init=0)
                if rw == 'send':
                    self.gpio.output_channel(pin=[EN_485],state=1)
                elif rw == 'recv':
                    self.gpio.output_channel(pin=[EN_485],state=0)                   
                else:
                    raise ValueError('Serial:only support recv or send')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok
    
    def send_msg(self, msg):
        if not self.demo:
            try:
                if self.mode == '485-manual':
                    self.mode_select('send')
                resp = self.instance.write(msg)
                self.instance.flush()
                logger.debug(f'Serial: send {resp} bytes with msg: {msg}')
                return self.status_ok
            except Exception as e:
                raise ValueError(e)
        else:
            return self.status_ok

    def recv_lines(self):
        if not self.demo:
            try:
                if self.mode == '485-manual':
                    self.mode_select('recv')
                self.instance.flushInput
                while self.instance.in_waiting() > 0:
                    resp = self.instance.readlines()
                    logger.debug(f'Serial: receive msg: {resp}')
                    return resp
            except Exception as e:
                raise ValueError(e)
        else:
            return [0]

    def recv_msg(self, len):
        if not self.demo:
            try:
                if self.mode == '485-manual':
                    self.mode_select('recv')
                self.instance.flushInput
                resp = self.instance.read(len)
                logger.debug(f'Serial: receive msg: {resp}')
                return resp
            except Exception as e:
                raise ValueError(e)
        else:
            return 0

    def recv_msg_until(self, ld):
        if not self.demo:
            try:
                if self.mode == '485-manual':
                    self.mode_select('recv')
                self.instance.flushInput
                resp = self.instance.read_until(ld)
                logger.debug(f'Serial: receive msg: {resp}')
                return resp
            except Exception as e:
                raise ValueError(e)
        else:
            return 0

# if __name__ == '__main__':
#     a = SerialHandler()
#     a.open_instr()
#     a.close_instr()