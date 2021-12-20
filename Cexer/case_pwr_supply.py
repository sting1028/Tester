import logging
import asyncio


logger = logging.getLogger(__name__)


async def run_power_supply_task(power_supply, cases, q):
        connected = False
        loop = cases['POWER_SUPPLY']['loop']
        delay = cases['POWER_SUPPLY']['delay']
        voltage = cases['POWER_SUPPLY']['voltage']
        current = cases['POWER_SUPPLY']['current']
        ocp = cases['POWER_SUPPLY']['ocp']
        ovp = cases['POWER_SUPPLY']['ovp']
        try:
            power_supply.connect()
            while (loop or not connected):
                power_supply.turn_off_output()
                power_supply.set_ocp(ocp)
                power_supply.set_ovp(ovp)
                power_supply.set_voltage(voltage)
                power_supply.set_current(current)
                power_supply.turn_on_output()
                if loop:
                    await asyncio.sleep(delay)
                    if connected == False:
                        q.put({'pwr_supply':{'case_complete': True, 'result': 'loop'}})
                connected = True
            q.put({'pwr_supply':{'case_complete': True, 'result': 'pass'}})
        except Exception as e:
            logger.info(e)
            q.put({'pwr_supply':{'case_complete': True, 'result': f'Error:{e}'}})
            raise RuntimeError(e)