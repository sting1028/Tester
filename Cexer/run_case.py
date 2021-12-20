
from pi.handler.gpio_handler import GpioHandler
from pi.handler.can_handler import CanHandler
from pi.handler.i2c_handler import I2cHandler
from pi.handler.serial_handler import SerialHandler
from pi.handler.serial_handler_async import SerialHandlerAsync
from pi.power_control import PowerSupply
from pi.scope_control import Scope
import logging, asyncio, json, time, threading, queue
from pathlib import Path
from case_can import run_can_poll
from case_serial import run_serial_task
from case_gpio import run_gpio_task
from case_pwr_supply import run_power_supply_task

logger = logging.getLogger(__name__)


def load_case(file):
    with Path(file).open() as js:
        return json.load(js)

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def close_instance(created_instr,cases):
    can = created_instr.get('can_instr')
    gpio = created_instr.get('gpio_instr')
    serial = created_instr.get('serial_instr')
    power_supply = created_instr.get('pwr_supply_instr')
    if can:
        can.close_instr()
    if gpio:
        gpio.release_channel(cases['GPIO']['pin'])
    if serial:
        serial.close_instr()
    if power_supply:
        power_supply.turn_off_output()
        power_supply.disconnect()

async def create_task_low_speed(cases,q,even_loop):
    init_task_result = {'case_complete': False, 'result': ''}
    if 'POWER_SUPPLY' in cases:
        power_supply = PowerSupply(model=cases['POWER_SUPPLY']['model'], addr=cases['POWER_SUPPLY']['addr'])
        q.put({'pwr_supply':init_task_result})
        q.put({'pwr_supply_instr':power_supply})
        await asyncio.create_task(run_power_supply_task(power_supply=power_supply, cases=cases, q=q))
    if 'GPIO' in cases:
        gpio = GpioHandler()
        q.put({'gpio':init_task_result})
        q.put({'gpio_instr':gpio})
        await asyncio.create_task(run_gpio_task(gpio=gpio,cases=cases,q=q))
    if 'SERIAL' in cases:
        if not gpio:
            gpio = GpioHandler()
        serial_projector = SerialHandlerAsync(gpio=gpio, interface=cases['SERIAL']['interface'])
        q.put({'serial':init_task_result})
        q.put({'serial_instr':serial_projector})
        await asyncio.create_task(run_serial_task(serial=serial_projector,cases=cases,q=q,even_loop=even_loop))

async def create_task_high_speed(cases,q,even_loop):
        init_task_result = {'case_complete': False, 'result': ''}
        can = CanHandler()
        q.put({'can':init_task_result})
        q.put({'can_instr':can})
        await asyncio.create_task(run_can_poll(can=can, cases=cases, q=q, even_loop=even_loop))

def run_task(cases,q):
    can_loop = object()
    other_loop = asyncio.new_event_loop()
    threading.Thread(target=start_loop,args=(other_loop,),daemon=True).start()
    asyncio.run_coroutine_threadsafe(create_task_low_speed(cases=cases,q=q,even_loop=other_loop),other_loop)
    if 'CAN' in cases:
        can_loop = asyncio.new_event_loop()
        threading.Thread(target=start_loop,args=(can_loop,),daemon=True).start()
        asyncio.run_coroutine_threadsafe(create_task_high_speed(cases=cases,q=q,even_loop=can_loop),can_loop)
    return other_loop, can_loop

def close_task(loops:list):
    for loop in loops:
        for task in asyncio.all_tasks(loop):
            task.cancel()
        while asyncio.all_tasks(loop):
            time.sleep(0.1)
        loop.call_soon_threadsafe(loop.stop)
        while loop.is_running():
            time.sleep(0.1)
        loop.close()
        while not loop.is_closed():
            time.sleep(0.1)

def check_case(q,cases):
    tasks_result = {}
    created_instr = {}
    case_finished = False
    while(not case_finished):
        queue_data = q.get()
        if 'can_instr' in queue_data:
            created_instr['can_instr'] = queue_data['can_instr']
        elif 'serial_instr' in queue_data:
            created_instr['serial_instr'] = queue_data['serial_instr']
        elif 'gpio_instr' in queue_data:
            created_instr['gpio_instr'] = queue_data['gpio_instr']
        elif 'pwr_supply_instr' in queue_data:
            created_instr['pwr_supply_instr'] = queue_data['pwr_supply_instr']

        elif 'can' in queue_data:
            tasks_result['can'] = queue_data['can']
        elif 'pwr_supply' in queue_data:
            tasks_result['pwr_supply'] = queue_data['pwr_supply']
        elif 'gpio' in queue_data:
            tasks_result['gpio'] = queue_data['gpio']
        elif 'serial' in queue_data:
            tasks_result['serial'] = queue_data['serial']
        logger.debug(f'queue:{queue_data}')
        logger.debug(f'task_result:{tasks_result}')
        if len(tasks_result) == len(cases):
            if all(tasks_result[task]['case_complete'] for task in tasks_result):
                    case_finished = True
    return created_instr, tasks_result

def check_result(results):
    final_result = []
    for result in results:
        for key in result['case_result']:
            if result['case_result'][key].get('result') in ['pass','loop']:
                final_result.append(True)
            else:
                final_result.append(False)
    if all(final_result):
        return 'pass'
    else:
        return 'failed'

def run_cases(case_file,q):
    try:
        logger.info(f'Case:{case_file.name} begin...')
        cases = load_case(case_file)
        other_loop, can_loop = run_task(cases=cases,q=q)
        created_instr, tasks_result = check_case(q,cases)
        close_task(loops=[other_loop,can_loop])
        close_instance(created_instr=created_instr, cases=cases)
        return {'case_name':case_file.name,'case_result':tasks_result}
    except Exception as e:
        raise RuntimeError(e)

def list_case_name():
    try:
        case_path = Path(__file__).parent.joinpath('case')
        case_name = [file.stem for file in case_path.iterdir()]
    except Exception as e:
        raise RuntimeError(e)
    return case_name
    
def main(case_name):
    try:
        results = []
        q = queue.Queue()
        case_path = Path(__file__).parent.joinpath('case')
        if case_name.upper() == 'ALL':
            for case in case_path.iterdir():
                case_result = run_cases(case_file=case, q=q)
                results.append(case_result)
        else:
            case_one = case_path.joinpath(f'{case_name}.json')
            case_result = run_cases(case_file=case_one, q=q)
            results.append(case_result)
        return {'final_result':check_result(results),'result_item':results}
            
    except Exception as e:
        raise RuntimeError(e)
    # finally:
    #     file_path = case_path.parent.joinpath('result.txt')
    #     if file_path.exists():
    #         file_path.unlink()
    #     with file_path.open('w') as f:
    #         f.writelines(result)


if __name__ == '__main__':
    from datetime import datetime
    import os,sys
    date_time = datetime.now().strftime('%Y.%m%d.%H%M')
    log_folder = Path('log/')
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    log_filename = f"{Path(f'log/{date_time}')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format=
        '{asctime} - {levelname} - {name} - {lineno} - {funcName} ::: {message}',
        filename=log_filename,
        style='{')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logger = logging.getLogger(__name__)
    main(case_name='case-can-connection')

