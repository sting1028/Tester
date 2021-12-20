import pylink,logging, time
from pi.power_control import PowerSupply

logger = logging.getLogger(__name__)

def flashMcu():
    pwr_supply = powerSupplyOn()
    jlink = connectJlink()
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    # jlink.set_tif(pylink.enums.JLinkResetStrategyCortexM3.core)
    jlink.connect('STM32F407ZE')
    logger.info(f'jlink connected:{jlink.target_connected()}')
    logger.info(f'jlink erase mem:{jlink.erase()}')
    logger.info('jlink start flash...')
    jlink.flash_file('/home/pi/Downloads/FLASH.bin', addr=0x8000000)
    logger.info('jlink start reset mcu...')
    jlink.set_reset_strategy(pylink.enums.JLinkResetStrategyCortexM3.CORE)
    print(jlink.reset(halt=False))
    logger.info('jlink wait 10s for mcu startup')
    time.sleep(10)
    powerSupplyOff(pwr_supply)

def connectJlink():
    jlink  = pylink.JLink()
    try:
        jlink.open()
        if jlink.connected():
            return jlink
        else:
            raise RuntimeError('JLINK not connected!')
    except Exception as e:
        raise RuntimeError(e)

def powerSupplyOn():
    try:
        power_supply = PowerSupply(model="citric", addr=34)
        power_supply.connect()
        power_supply.turn_off_output()
        power_supply.set_ocp(4)
        power_supply.set_ovp(60)
        power_supply.set_voltage(24)
        power_supply.set_current(2)
        power_supply.turn_on_output()
    except Exception as e:
        raise RuntimeError(e)
    return power_supply

def powerSupplyOff(instr):
    instr.turn_off_output()
    instr.disconnect()
    
if __name__ == '__main__':
    flashMcu()