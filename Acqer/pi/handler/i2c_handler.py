import logging,struct
from smbus2 import SMBus, i2c_msg
logger = logging.getLogger(__name__)


class I2cHandler:
    def __init__(self, demo=False):
        self.instance = None
        self.demo = demo
        self.status_ok = {'status': 'ok'}

    def open_instr(self, port=1):
        if not self.demo:
            try:
                self.instance = SMBus(port)
                self.instance.open(f'/dev/i2c-{port}')
                logger.debug(f'I2C: /dev/i2c-{port} opened!')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok

    def close_instr(self):
        if not self.demo:
            try:
                self.instance.close()
                logger.debug('I2C: /dev/i2c-1 closed!')
                self.instance = None
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok
    
    def recv_i2c_byte(self, address):
        """ recv a byte data from instrument address"""
        if not self.demo:
            try:
                resp = self.instance.recv_byte(address)
                logger.debug(f'I2C: recv from instruments:{address}: {resp}')
                return resp
            except Exception as e:
                raise IOError(e)
        else:
            return -1

    def send_i2c_byte(self, address, value):
        """send a byte to instrument address"""
        if not self.demo:
            try:
                self.instance.send_byte(address, value)
                logger.debug(f'I2C: send to instruments:{address} : {value}')
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok

    def send_i2c_bytes(self, address, value):
        """send a bytes list to i2c address"""
        if not self.demo:
            try:
                msg = i2c_msg.send(address, value)
                self.instance.i2c_rdwr(msg)
                logger.debug(f"I2C: send {value} to I2C {address:#x}")
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok

    def send_reg_U8(self, address, reg, value):
        """send a byte to a given register"""
        if not self.demo:
            try:
                self.instance.send_byte_data(address, reg, value)
                logger.debug(f'I2C: send to instruments:{address} reg: {reg} value: {value}')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok 

    def recv_reg_U8(self, address, reg):
        """recv a single byte from a designated register"""
        if not self.demo:
            try:
                result = self.instance.recv_byte_data(address, reg)
                logger.debug(
                        f"I2C: Returned {result:#x} from register {reg:#x}")
                return result
            except Exception as e:
                raise IOError(e)
        else:
            return -1

    def recv_reg_S16(self, address, reg):
        """recv a signed 16-bit value from the I2C device"""
        if not self.demo:
            try:
                hibyte = self.instance.recv_byte_data(address, reg)
                if (hibyte > 127):
                    hibyte -= 256
                result = (hibyte << 8) + self.instance.recv_byte_data(
                    address, reg + 1)
                logger.debug(
                        f"I2C: Returned {result:#x} from register {reg:#x}")
                return result
            except Exception as e:
                raise IOError(e)
        else:
            return -1

    def recv_reg_U16(self, address, reg):
        """recv an unsigned 16-bit value from the I2C device"""
        if not self.demo:
            try:
                hibyte = self.instance.recv_byte_data(address, reg)
                result = (hibyte << 8) + self.instance.recv_byte_data(
                    address, reg + 1)
                logger.debug(
                        f"I2C: Returned {result:#x} from register {reg:#x}")
                return result
            except Exception as e:
                raise IOError(e)
        else:
            return -1

    def recv_reg_BlockData(self, address, reg, length):
        """recv register block data with length"""
        if not self.demo:
            try:
                result = self.instance.recv_i2c_block_data(address, reg, length)
                logger.debug(
                        f"I2C: Returned {result} from register {reg:#x}")
                return result
            except Exception as e:
                raise IOError(e)
        else:
            return -1

    def send_reg_Block(self, address, reg, value):
        """send block to i2c register"""
        if not self.demo:
            try:
                self.instance.send_i2c_block_data(address, reg, value)
                logger.debug(f"I2C: send {value} to register {reg:#x}")
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok


# if __name__ == '__main__':
#     a = I2cHandler()
#     a.open_instr()
#     a.close_instr()