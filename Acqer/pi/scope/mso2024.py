import logging
logger = logging.getLogger(__name__)

class Mso2024:
    def __init__(self):
        self.status_ok = {'status': 'ok'}

    def save_screenshot(self, visa, file_name):
        try:
            # screenshot = self.instance.query_binary_values('CURVe?', datatype='d')
            visa.send_cmd('SAVe:IMAGe \"E:/Temp.png\"')
            visa.opc()
            visa.send_cmd('FILESystem:READFile \"E:/Temp.png\"')
            screenshot = visa.recv_raw(1024*1024)
        except RuntimeError as ee:
            raise RuntimeError(ee)
        except IOError as e:
            raise IOError(e)
        else:
            with open(file_name, 'wb') as f:
                f.write(bytes(screenshot))
            logger.info(f'{file_name} saved!')
            visa.send_cmd('FILESystem:DELEte \"E:/Temp.png\"')
            return self.status_ok

    def set_horizontal(self, visa, time=2E-6):
        # default set the time 2us if time is not given
        try:
            visa.send_cmd(f'HORizontal:SCALE {time}')
            return self.status_ok
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)

    def set_vertical(self, visa, ch=1, vol=100E-03):
        # default set the voltage 100mV if vol is not given
        try:
            visa.send_cmd(f'CH{ch}:SCALE {vol}')
            return self.status_ok
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)

    def set_bw(self, visa, ch=1, bw='FUL'):
        # default set the bw full if bw is not given, support 'FUL'/'TWE'
        try:
            visa.send_cmd(f'CH{ch}:BANdwidth {bw}')
            return self.status_ok
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)
    
    def set_couping(self, visa, ch=1, coup='DC'):
        # default set the coup is 'DC' if coup is not given, support 'AC','DC','GND'
        try:
            visa.send_cmd(f'CH{ch}:COUPling {coup}')
            return self.status_ok
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)
    
    def set_label(self, visa, ch=1, label='1'):
        # the text string is limited to 30 characters
        try:
            visa.send_cmd(f'CH{ch}:LABel {label}')
            return self.status_ok
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)

    def set_offset(self, visa, ch=1, offset=0):
        # for V/Div settings from 2mV/div to 200mV/div, the offset range is +/- 1V
        # for V/Div settings from 202mV/div to 5V/div, the offset range is +/- 25V
        try:
            visa.send_cmd(f'CH{ch}:OFFSet {offset}')
            return self.status_ok
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)
    
    def get_waveform(self, visa, ch):
        try:
            visa.send_cmd('ACQ:STATE OFF')
            visa.send_cmd(f'DATa:RESOlution FULL :DATa:SOUrce {ch}')
            wfm = visa.recv_raw('WAVFrm?')
            logger.info (wfm)
            # self.instance.query_binary_values('CURVe?', datatype='d')
            visa.send_cmd('ACQ:STATE ON')
            
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)

    def get_info(self, visa):
        try:
            return visa.recv_value('*IDN?')
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)