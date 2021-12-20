from .handler.serial_handler import SerialHandler
import logging
import importlib
logger = logging.getLogger(__name__)


class PowerSupply:
    def __init__(self, model, demo=False, addr=256):
        self.demo = demo
        self.model = model
        self.info = ''
        self.power_supply = None
        self.instr = None
        self.status_ok = {'status': 'ok'}
        self.addr = addr
    
    def connect(self):
            try:
                params = importlib.import_module(f'.{self.model.lower()}', package='pi.powerSupply')
                func = getattr(params, self.model.capitalize())
                self.power_supply = func(addr=self.addr)
                if self.model.upper() == 'CITRIC':
                    self.instr = SerialHandler(demo=self.demo,interface='/dev/ttyS0')
                    self.instr.open_instr(mode='485-auto',bitrate=19200,bytesize=8,parity='none')
                    self.info = self.get_info()
                else:
                    raise ValueError('Please input correct model info, CITRIC')
            except IOError as e:
                raise IOError(e)
            except RuntimeError as ee:
                raise RuntimeError(ee)
            else:
                logger.info(f'Connect to {self.info} successful!')
                return self.status_ok
        
    def disconnect(self):
            try:
                self.instr.close_instr()
            except IOError as e:
                raise IOError(e)
            else:
                logger.info(f'{self.info} Disconnected!')
        
    def set_voltage(self, voltage):
            try:
                resp = self.power_supply.set_voltage(instr=self.instr,voltage=voltage)
                logger.info(f'PowerSupply: set voltage:{voltage}V')
                return resp
            except IOError as e:
                raise IOError(e)
        
    def read_set_voltage(self):
            try:
                resp = self.power_supply.read_set_voltage(instr=self.instr)
                logger.info(f'PowerSupply: read set voltage:{resp}V')
            except Exception as e:
                raise IOError(e)

    def read_set_current(self):
            try:
                resp = self.power_supply.read_set_current(instr=self.instr)
                logger.info(f'PowerSupply: read set current:{resp}A')
                return resp
            except Exception as e:
                raise IOError(e)
        
    def set_current(self, current):
            try:
                resp = self.power_supply.set_current(instr=self.instr,current=current)
                logger.info(f'PowerSupply: set current:{current}A')
                return resp
            except Exception as e:
                raise IOError(e)
        
    def set_ocp(self, current):
            try:
                resp = self.power_supply.set_ocp(instr=self.instr, ocp=current)
                logger.info(f'PowerSupply: set OCP:{current}A')
                return resp
            except Exception as e:
                raise IOError(e)

    def set_ovp(self,voltage):
            try:
                resp = self.power_supply.set_ovp(instr=self.instr, ovp=voltage)
                logger.info(f'PowerSupply: set OVP:{voltage}V')
                return resp
            except Exception as e:
                raise IOError(e)

    def turn_on_output(self):
            try:
                resp = self.power_supply.turn_on_output(instr=self.instr)
                logger.info(f'PowerSupply: output is turn on')
                return resp
            except Exception as e:
                raise IOError(e)

    def turn_off_output(self):
            try:
                resp =  self.power_supply.turn_off_output(instr=self.instr)
                logger.info(f'PowerSupply: output is turn off')
                return resp
            except Exception as e:
                raise IOError(e)
        
    def get_info(self):
            try:
                return self.power_supply.get_info(instr=self.instr)
            except IOError as e:
                raise IOError(e)
            except RuntimeError as ee:
                raise RuntimeError(ee)
        
    # async def get_opc(self):
    #         try:
    #             return await self.power_supply.get_opc(instr=self.instr)
    #         except IOError as e:
    #             raise IOError(e)
    #         except RuntimeError as ee:
    #             raise RuntimeError(ee)

if __name__ == '__main__':
    pwr = PowerSupply(model='citric',addr=34)
    pwr.connect()
    pwr.set_ocp(2)
    pwr.disconnect()



