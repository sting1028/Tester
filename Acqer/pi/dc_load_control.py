import os
from .handler.visa_handler import VisaHandler
import logging
import importlib
logger = logging.getLogger(__name__)


class DcLoad:
    def __init__(self, model, demo=False):
        self.demo = demo
        self.model = model
        self.load = None
        self.info = None
        if model.upper() == 'IT8912E':
            self.visa_addr = 'USB0::65535::35090::602095010716910004'
        else:
            raise ValueError('Please input correct model info, only support IT8912E now')
        self.visa = VisaHandler(visa_addr=self.visa_addr, demo=demo)
    
    def connect(self):
        try:
            params = importlib.import_module(f'.{self.model.lower()}', package='pi.dcLoad')
            func = getattr(params, self.model.capitalize())
            self.load = func()
            return self.visa.open_instr()
        except IOError as e:
            raise IOError(e)
        else:
            logger.info(f'Connect to {self.get_info()} successful!')
    
    def disconnect(self):
        try:
            return self.visa.close_instr()
        except IOError as e:
            raise IOError(e)
        else:
            logger.info(f'{self.info} Disconnected!')
    
    def reset(self):
        try:
            resp1 = self.load.reset(visa=self.visa)
            resp2 = self.load.clear_error(visa=self.visa)
            resp3 = self.load.enable_output(visa=self.visa,onff='off')
            return self.merge_response([resp1,resp2])
        except IOError as e:
            raise IOError(e)
    
    def get_info(self):
        try:
            self.info = self.load.get_info(visa=self.visa)
        except IOError as e:
            raise IOError(e)
        else:
            return self.info
    
    def get_error_info(self):
        try:
            return self.load.get_error(visa=self.visa)
        except IOError as e:
            raise IOError(e)
    
    def set_mode(self,mode):
        try:
            return self.load.set_mode(visa=self.visa,mode=mode)
        except IOError as e:
            raise IOError(e)
        else:
            return self.info
        
    def enable_output(self,onff):
        try:
            return self.load.enable_output(visa=self.visa,onff=onff)
        except IOError as e:
            raise IOError(e)
    
    def set_cv_voltage(self,voltage):
        try:
            return self.load.set_cv_voltage(visa=self.visa,voltage=voltage)
        except IOError as e:
            raise IOError(e)

    def set_cc_current(self,current):
        try:
            return self.load.set_cc_current(visa=self.visa,current=current)
        except IOError as e:
            raise IOError(e)
    
    def set_cr_resistance(self,res):
        try:
            return self.load.set_cr_res(visa=self.visa,res=res)
        except IOError as e:
            raise IOError(e)
    
    def set_cp_power(self,pow):
        try:
            return self.load.set_cp_pow(visa=self.visa,pow=pow)
        except IOError as e:
            raise IOError(e)

    def set_current_slew(self,pos,neg):
        try:
            return self.load.set_current_slew(visa=self.visa,pos=pos,neg=neg)
        except IOError as e:
            raise IOError(e)

    def set_cc_tran(self,alev,blev,awid,bwid):
        try:
            resp1 = self.load.set_cc_tran_CONT(visa=self.visa)
            resp2 = self.load.set_cc_tran(visa=self.visa,alev=alev,blev=blev,awid=awid,bwid=bwid)
            return self.merge_response([resp1,resp2])
        except IOError as e:
            raise IOError(e)
    
    def enable_tran(self,onff):
        try:
            resp1 = self.load.enable_tran(visa=self.visa,onff=onff)
            resp2 = self.load.en_trig(visa=self.visa)
            return self.merge_response([resp1,resp2])
        except IOError as e:
            raise IOError(e)
    
    def set_led(self,range,volt,curr,coef,freq,duty):
        try:
            return self.load.set_led(visa=self.visa,range=range,volt=volt,current=curr,coef=coef,freq=freq,duty=duty)
        except IOError as e:
            raise IOError(e)
    
    def merge_response(self, resps):
        try:
            if all(i['status'] == 'ok' for i in resps):
                return {'status': 'ok'}
            else:
                return {'status': 'nok'}
        except Exception as e:
            raise IOError(e)

