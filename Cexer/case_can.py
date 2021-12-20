import logging, time
import asyncio
from async_timeout import timeout

logger = logging.getLogger(__name__)

async def run_can_poll(can, cases, q,even_loop):
    cases_trx =cases['CAN']['polling_datas']
    loop = cases['CAN']['loop']
    case_trx_item = [i['comment'] for i in cases_trx]
    checked_trx_item = []
    case_complete= False
    loop_timeout = False
    index = 0
    try:
        can.open_instr()
        time_start = time.time()
        while(loop or not case_complete):
            if not loop_timeout:
                time_now = time.time()
                async with timeout(cases['CAN']['case_timeout']):
                    last_msg_recv = await can.receive_notify(loop=even_loop)
                # logger.debug(f'can:recved_msg:{last_msg_recv}')
                for case in (cases_trx):
                    recv_id = case['receive']['id']
                    recv_data = case['receive']['data']
                    if last_msg_recv.arbitration_id == recv_id:
                        if last_msg_recv.data[0] == bytearray(recv_data)[0]:
                        # await asyncio.sleep(case['delay'])
                            for i in case['send']:
                                send_id = i['id']
                                if i['data']:
                                    send_data = i['data']
                                else:
                                    if 'append' in i:
                                        last_msg_recv.data.extend(i['append'])
                                    send_data = last_msg_recv.data
                                can.send_msg(id=send_id, data=send_data, timeout=cases['CAN']['send_timeout'])
                                # logger.info(f'can:send_msg: id:{send_id}, data:{send_data}')
                                # await {'case_complete': True, 'result': 'looping'}
                                if not loop and not case_complete:
                                    checked_trx_item.append(case['comment'])
            else:
                raise RuntimeError('Timeout')
            if not loop:
                if time_now - time_start >= cases['CAN']['case_timeout']:
                    loop_timeout = True
                    q.put({'can':{'case_complete': True, 'result': 'timeout'}})
                    logger.info('Can poll case check timeout')
                else:
                    if set(case_trx_item) <= set(checked_trx_item):
                        case_complete = True
                        logger.info('Can poll case check passed!')
                        q.put({'can':{'case_complete': True, 'result': 'pass'}})
                    else:
                        q.put({'can':{'case_complete': False, 'result': ''}})
            else:
                if not case_complete:
                    q.put({'can':{'case_complete': True, 'result': 'loop'}})
                case_complete = True
                # index += 1
                # print(f'can_index:{index}')
    except Exception as e:
        logger.info(e)
        q.put({'can':{'case_complete': True, 'result': f'Error:{e}'}})
        raise IOError(e)

async def run_can_send(can,cases):
    read_continue = True
    while (read_continue):
        for i in cases['CAN']['send_active']['send']:
            can.send_msg(id=i['id'], data=i['data'])
            await asyncio.sleep(cases['CAN']['send_active']['delay'])