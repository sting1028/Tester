import asyncio
import logging
from async_timeout import timeout

logger = logging.getLogger(__name__)

async def run_serial_task(serial,cases,q,even_loop):
        datas = cases['SERIAL']['datas']
        loop = cases['SERIAL']['loop']
        loop_delay = cases['SERIAL']['loop_delay']
        pre_delay = cases['SERIAL']['pre_delay']
        connected = False
        response = {'status':[], 'result':[]}
        try:
            logger.info(f'serial: please wait for {pre_delay}s')
            await asyncio.sleep(pre_delay)
            await serial.open_instr(mode='usb',bitrate=9600,bytesize=8,parity='even',even_loop=even_loop)
            while(loop or not connected):
                for data in datas:
                    if 'delay' in data:
                        await asyncio.sleep(data['delay'])
                    serial.send_msg(bytes(data['tx']))
                    await asyncio.sleep(data['delay'])
                    # resp = await serial.recv_msg(len=len(data['rx']))
                    async with timeout(cases['SERIAL']['timeout']):
                        resp = await serial.recv_msg_until(b'\r')
                    want_data = bytes(data['rx'])
                    if resp == want_data:
                        logger.info('serial: received msg correct!')
                        response['status'].append(True)
                    else:
                        failed_item = f'serial recv msg:{resp}, want:{want_data}'
                        response['result'].append(failed_item)
                        logger.info (f'serial: received msg incorrect!{failed_item}')
                        response['status'].append(False)
                if not loop:
                    if all(response['status']):
                        logger.info (f'serial case check passed!')
                        q.put({'serial':{'case_complete': True, 'result': 'pass'}})
                    else:
                        logger.info (f'serial case check failed!')
                        q.put({'serial':{'case_complete': True, 'result': 'failed', 'failedItem':response['result']}})
                else:
                    if connected == False:
                        q.put({'serial':{'case_complete': True, 'result': 'loop'}})
                    await asyncio.sleep(loop_delay)
                connected = True
        except Exception as e:
            logger.info(e)
            q.put({'serial':{'case_complete': True, 'result': f'Error:{e}'}})
            raise RuntimeError(e)