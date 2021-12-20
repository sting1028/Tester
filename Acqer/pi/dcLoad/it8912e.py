import logging
logger = logging.getLogger(__name__)


class It8912e:
    def __init__(self):
        pass

    def get_info(self, visa):
        try:
            return visa.recv_value('*IDN?')
        except IOError as e:
            raise IOError(e)
    
    def clear_error(self, visa):
        try:
            resp = visa.send_cmd('SYST:CLE')
            self.try_opc(visa)
            return resp
        except IOError as e:
            raise IOError(e)
    
    def get_opc(self,visa):
        try:
            resp = visa.recv_value('*OPC?')
            self.try_opc(visa)
            return resp
        except IOError as e:
            raise IOError(e)
    
    def reset(self,visa):
        try:
            resp = visa.send_cmd('*RST')
            self.try_opc(visa)
            return resp
        except IOError as e:
            raise IOError(e)
    
    def get_error(self,visa):
        try:
            resp = visa.recv_value('SYST:ERR?')
            self.try_opc(visa)
            return resp
        except IOError as e:
            raise IOError(e)
    
    def meas_voltage(self, visa):
        try:
            return visa.recv_value('MEAS:VOLT?')
        except IOError as e:
            raise IOError(e)
    
    def meas_current(self, visa):
        try:
            return visa.recv_value('MEAS:CURR?')
        except IOError as e:
            raise IOError(e)
    
    def enable_short(self,visa,onff):
        try:
            resp = visa.send_cmd(f'INP:SHOR {onff.upper()}')
            self.try_opc(visa)
            return resp
        except IOError as e:
            raise IOError(e)
    
    def enable_output(self,visa,onff):
        try:
            resp = visa.send_cmd(f'INP {onff.upper()}')
            self.try_opc(visa)
            return resp
        except IOError as e:
            raise IOError(e)

    def set_mode(self, visa, mode):
        table = {
            'CC': 'CURR',
            'CV': 'VOLT',
            'CR': 'RES',
            'LED': 'LED',
            'CP': 'POW'
        }
        try:
            resp1 = visa.send_cmd('FUNC:MODE FIX')
            resp2 = visa.send_cmd(f'FUNC {table[mode.upper()]}')
            self.try_opc(visa)
            return self.merge_response([resp1,resp2])
        except Exception as e:
            raise IOError(e)
    
    def enable_tran(self, visa, onff):
        try:
            resp = visa.send_cmd(f'TRAN {onff.upper()}')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)

    def clear_protec(self, visa):
        try:
            resp = visa.send_cmd('INP:PROT:CLE')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)

    def set_cc_current(self, visa, current):
        try:
            resp = visa.send_cmd(f'CURR {current}')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)
    
    def set_current_slew(self, visa, pos, neg):
        """0-3A: 0.0001~0.3A/us
            0-15A: 0.001~1.5A/us"""
        try:
            resp = visa.send_cmd(f'CURR:SLEW:POS {pos};NEG {neg}')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)

    def set_ocp(self, visa, current):
        try:
            resp = visa.send_cmd(f'CURR:PROT {current}')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)
    
    def enable_ocp(self, visa, onff):
        try:
            resp = visa.send_cmd(f'CURR:PROT:STAT {onff.upper()}')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)
    
    def set_cc_tran(self,visa,alev,blev,awid,bwid):
        try:
            resp = visa.send_cmd(f'CURR:TRAN:ALEV {alev};BLEV {blev};AWID {awid};BWID {bwid}')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)
    
    def set_cc_tran_CONT(self,visa):
        try:
            resp = visa.send_cmd(f'CURR:TRAN:MODE CONT')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)
    
    def set_cv_voltage(self,visa,voltage):
        try:
            resp = visa.send_cmd(f'VOLT {voltage}')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)
    
    def set_cr_res(self,visa,res):
        try:
            resp = visa.send_cmd(f'RES {res}')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)
    
    def set_cp_pow(self,visa,pow):
        try:
            resp = visa.send_cmd(f'POW {pow}')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)
    
    def set_led(self,visa,range,volt,current,coef,freq,duty):
        """range: 0 for low_volt_level(0-100), 1 for high_volt_level(0-500)"""
        try:
            resp = visa.send_cmd(f'LED:RANG {range};VOLT {volt};CURR {current};COEF {coef};FREQ {freq};DUTY {duty}')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)
    
    def en_trig(self,visa):
        try:
            resp = visa.send_cmd('TRIG')
            self.try_opc(visa)
            return resp
        except Exception as e:
            raise IOError(e)

    def merge_response(self, resps):
        try:
            if all(i['status'] == 'ok' for i in resps):
                return {'status': 'ok'}
            else:
                return {'status': 'nok'}
        except Exception as e:
            raise IOError(e)
    
    def try_opc(self,visa):
        for i in range(6):
            resp = visa.opc()
            if resp != b'1\n':
                 time.sleep(0.1)
            else:
                break