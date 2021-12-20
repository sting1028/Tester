
from dc_load_control import DcLoad
from power_control import PowerSupply
import time, os, logging, sys
from datetime import datetime
from pathlib import Path

def log_config():
    date_time = datetime.now().strftime('%Y%m%d%H%M%S')
    log_folder = Path('log/')
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    log_filename = f"{Path(f'log/{date_time}')}.log"
    logging.basicConfig(
        level=logging.DEBUG,
        format=
        '{asctime} - {levelname} - {name} - {lineno} - {funcName} ::: {message}',
        filename=log_filename,
        style='{')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))



if __name__ == '__main__':
    try:
        dc_load = DcLoad(model='it8912e')
        mode = 'cc'
        power_supply = PowerSupply(model='citric', addr=34)
        
        log_config()
        dc_load.connect()
        print(dc_load.get_info())
        dc_load.reset()
        power_supply.connect()
        power_supply.turn_off_output()
        power_supply.set_ocp(6)
        power_supply.set_ovp(50)
        power_supply.set_voltage(48)
        power_supply.set_current(4)
        power_supply.turn_on_output()
 
        for i in range(10000):
            if mode == 'tran':
                # dc_load.set_mode('cc')
                dc_load.set_cc_tran(alev=0.1,blev=1.8, awid=0.005, bwid=0.005)
                dc_load.enable_tran('on')
                dc_load.set_current_slew(pos=0.3, neg=0.3)
            else:
                dc_load.set_mode(mode)
            if mode == 'led':
                dc_load.set_led(range=0, volt=30, curr=3, coef=0.1, freq=250, duty=0.1)
            elif mode == 'cc':
                dc_load.set_cc_current(2)
            elif mode == 'cv':
                dc_load.set_cv_voltage(voltage)
            elif mode =='cr':
                dc_load.set_cr_resistance(res)
            dc_load.enable_output('on')
            time.sleep(10)
            dc_load.enable_output('off')
            dc_load.enable_tran('off')
            time.sleep(1)
            print(f'mode:{mode}')
            if i%2 == 0:
                mode = 'tran'
            else:
                mode = 'cc'
            print(dc_load.get_error_info())
    except Exception as e:
        raise RuntimeError(e)
    finally:
        dc_load.disconnect()
        power_supply.disconnect()
        power_supply.turn_off_output()