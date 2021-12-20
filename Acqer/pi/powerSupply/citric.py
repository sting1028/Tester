import logging,time
logger = logging.getLogger(__name__)

class Citric:
    def __init__(self, addr):
        self.addr = addr

    def set_voltage(self, instr, voltage):
            try:
                cmd = f':VOLT {voltage}\n'
                resp = instr.send_msg(bytes([self.addr]) + cmd.encode())
                self.try_opc(instr)
                return resp
            except Exception as e:
                raise IOError(e)

    def set_current(self, instr, current):
            try:
                cmd = f':CURR {current}\n'
                resp = instr.send_msg(bytes([self.addr]) + cmd.encode())
                self.try_opc(instr)
                return resp
            except Exception as e:
                raise IOError(e)
        
    def read_set_voltage(self, instr):
            try:
                cmd = b':VOLT?\n'
                instr.send_msg(bytes([self.addr]) + cmd)
                resp = instr.recv_msg_until(b'\n')
                self.try_opc(instr)
                return resp
            except Exception as e:
                raise IOError(e)
        
    def read_set_current(self, instr):
            try:
                cmd = b':CURR?\n'
                instr.send_msg(bytes([self.addr]) + cmd)
                resp = instr.recv_msg_until(b'\n')
                self.try_opc(instr)
                return resp
            except Exception as e:
                raise IOError(e)
        
    def set_ovp(self, instr, ovp):
            try:
                cmd_set = f':VOLT:PROT:LEV {ovp}\n'
                cmd_en = f':VOLT:PROT:STAT ON\n'
                resp1 = instr.send_msg(bytes([self.addr]) + cmd_set.encode())
                self.try_opc(instr)
                resp2 = instr.send_msg(bytes([self.addr]) + cmd_en.encode())
                self.try_opc(instr)
                self.merge_response([resp1,resp2])
            except Exception as e:
                raise IOError(e)
        
    def set_ocp(self, instr, ocp):
            try:
                cmd_set = f':CURR:PROT:LEV {ocp}\n'
                cmd_en = f':CURR:PROT:STAT ON\n'
                resp1 = instr.send_msg(bytes([self.addr]) + cmd_set.encode())
                self.try_opc(instr)
                resp2 = instr.send_msg(bytes([self.addr]) + cmd_en.encode())
                self.try_opc(instr)
                self.merge_response([resp1,resp2])
            except Exception as e:
                raise IOError(e)

    def turn_on_output(self, instr):
            try:
                cmd = b':OUTP ON\n'
                resp = instr.send_msg(bytes([self.addr]) + cmd)
                self.try_opc(instr)
                return resp
            except Exception as e:
                raise IOError(e)

    def turn_off_output(self, instr):
            try:
                cmd = b':OUTP OFF\n'
                resp = instr.send_msg(bytes([self.addr]) + cmd)
                self.try_opc(instr)
                return resp
            except Exception as e:
                raise IOError(e)
        
    def measure_voltage(self, instr):
            try:
                cmd = b':MEAS:VOLT?\n'
                instr.send_msg(bytes([self.addr]) + cmd)
                resp = instr.recv_msg_until(b'\n')
                self.try_opc(instr)
                return resp
            except Exception as e:
                raise IOError(e)
        
    def measure_current(self, instr):
            try:
                cmd = b':MEAS:CURR?\n'
                resp = instr.recv_msg_until(b'\n')
                self.try_opc(instr)
                return resp
            except Exception as e:
                raise IOError(e)
        
    def measure_power(self, instr):
            try:
                cmd = b':MEAS:POW?\n'
                instr.send_msg(bytes([self.addr]) + cmd)
                resp = instr.recv_msg_until(b'\n')
                self.try_opc(instr)
                return resp
            except Exception as e:
                raise IOError(e)

    def get_info(self, instr):
            try:
                cmd = b'*IDN?\n'
                instr.send_msg(bytes([self.addr]) + cmd)
                resp = instr.recv_msg_until(b'\n')
                self.try_opc(instr)
                return resp
            except Exception as e:
                raise IOError(e)
        
    def get_opc(self, instr):
            try:
                cmd = b'*OPC?\n'
                instr.send_msg(bytes([self.addr]) + cmd)
                return instr.recv_msg_until(b'\n')
                # await "{:.0f}".format(int(resp.decode()))
            except Exception as e:
                raise IOError(e)

    def try_opc(self,instr):
        try:
            for i in range(5):
                resp = self.get_opc(instr)
                if resp != b'1\n':
                    time.sleep(0.3)
                else:
                    break
                if i >= 4:
                    raise IOError('OPC time out')
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