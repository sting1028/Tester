import pyvisa as visa
import logging
logger = logging.getLogger(__name__)

class VisaHandler:
    def __init__(self, visa_addr, demo=False):
        #self.visa_dll = 'c:/windows/system32/visa32.dll'
        self.demo = demo
        self.visa_dll = '@py'
        self.visa_addr = visa_addr
        self.instance = None
        self.instance_number = 0
        self.status_ok = {'status': 'ok'}
        # self.response = {'status': 'ok', 'resp': object}
    
    def open_instr(self):
        if not self.demo:
            try:
                self.instance = visa.ResourceManager(self.visa_dll).open_resource(self.visa_addr)
                self.instance.timeout = 10000
                self.instance_number += 1
                logger.debug(f'VISA:instance{self.instance_number} opened for {self.visa_addr}')
                return self.status_ok
            except visa.errors.VisaIOError as e:
                raise IOError(e)
            except RuntimeError as ee:
                raise RuntimeError(ee)
        else:
            return self.status_ok

    def close_instr(self):
        if not self.demo:
            try:
                if self.instance is not None:
                    self.instance.close()
                    self.instance = None
                    logger.debug(f'VISA:instance{self.instance_number} closed')
                    return self.status_ok 
            except visa.errors.VisaIOError as e:
                raise IOError(e)
            except Exception as ee:
                raise RuntimeError(ee)
        else:
            return self.status_ok

    def send_cmd(self, cmd):
        if not self.demo:
            try:
                self.instance.write(cmd)
                logger.debug(f'VISA:command: {cmd} send!')
                return self.status_ok 
            except visa.errors.VisaIOError as e:
                raise IOError(e)
            except Exception as ee:
                raise RuntimeError(ee)            
        else:
            return self.status_ok

    def recv_value(self, cmd):
        if not self.demo:
            try:
                logger.debug(f'VISA:command: {cmd} send!')
                resp = self.instance.query(cmd)
                logger.debug(f'VISA:data: {resp} received!')
                return resp
            except visa.errors.VisaIOError as e:
                raise IOError(e)
            except Exception as ee:
                raise RuntimeError(ee)
        else:
            return -1

    def recv_binary_values(self, cmd):
        if not self.demo:
            try:
                logger.debug(f'VISA:command: {cmd} send!')
                resp = self.instance.binary_values(cmd)
                logger.debug(f'VISA:data: {resp} received!')
                return resp
            except visa.errors.VisaIOError as e:
                raise IOError(e)
            except Exception as ee:
                raise RuntimeError(ee)   
        else:
            return -1
    
    def recv_raw(self, cmd):
        if not self.demo:
            try:
                logger.debug(f'VISA:command: {cmd} send!')
                resp = self.instance.read_raw(cmd)
                logger.debug(f'VISA:data: {resp} received!')
                return resp
            except visa.errors.VisaIOError as e:
                if self.instance.last_status.name == 'error_timeout':
                    raise IOError('VISA:Please Check USB disk is inserted or Instruments is connected')
                else:
                    raise IOError(e)
            except Exception as ee:
                raise RuntimeError(ee)
        else:
            return 0
    
    def opc(self):
        if not self.demo:
            try:
                resp = self.instance.query('*OPC?')
                logger.debug(f'VISA:opc result: {resp}')
                return resp
            except visa.errors.VisaIOError as e:
                raise IOError(e)
            except Exception as ee:
                raise RuntimeError(ee)
        else:
            return 1