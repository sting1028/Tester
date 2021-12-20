import logging
import asyncio

logger = logging.getLogger(__name__)

async def run_gpio_task(gpio,cases,q):
        pins = cases['GPIO']['pin']
        init_state = cases['GPIO']['init_level']
        duration = cases['GPIO']['duration']
        loop = cases['GPIO']['loop']
        connected = False
        try:
            gpio.setup_channel_out(pin=pins,init=init_state)
            while(loop or not connected):
                gpio.output_channel(pin=pins,state=init_state)
                if loop == True:
                    await asyncio.sleep(duration)
                    gpio.output_channel(pin=pins,state= not init_state)
                    await asyncio.sleep(duration)
                    if connected == False:
                        q.put({'gpio':{'case_complete': True, 'result': 'pass'}})
                connected = True
                q.put({'gpio':{'case_complete': True, 'result': 'pass'}})
        except Exception as e:
            logger.info(e)
            q.put({'gpio':{'case_complete': True, 'result': f'Error:{e}'}})
            raise RuntimeError(e)
