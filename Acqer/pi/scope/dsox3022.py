import logging
logger = logging.getLogger(__name__)


class Dsox3022:
    def __init__(self):
        pass

    def save_screenshot(self, visa, file_name):
        try:
            visa.send_cmd(':HARDcopy:INKSaver OFF')
            screenshot = visa.recv_binary_values(':DISPlay:DATA? PNG, COLor', datatype='s')
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)
        else:
            with open(file_name, 'wb') as f:
                f.write(bytes(screenshot))
            logger.info(f'{file_name} saved!')
    
    def get_info(self, visa):
        try:
            return visa.recv_value('*IDN?')
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)