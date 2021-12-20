import os
from .handler.visa_handler import VisaHandler
import logging
import importlib
logger = logging.getLogger(__name__)


class Scope:
    def __init__(self, model, demo=False):
        self.demo = demo
        self.model = model
        self.dso = None
        self.info = None
        if model.upper() == 'DSOX3022':
            self.visa_addr = 'USB0::10893::5991::MY56310121::INSTR'
        elif model.upper() == 'MSO2024':
            self.visa_addr = 'USB0::1689::932::C030730::INSTR'
        else:
            raise ValueError('Please input correct model info, DSOX3022 or MSO2024')
        self.visa = VisaHandler(visa_addr=self.visa_addr, demo=demo)
    
    def gen_file_name(self):
        try:
            pic_names = []
            file_names = os.listdir()
            for file_name in file_names:
                if '.png' in file_name:
                    pic_names.append(file_name)
            if pic_names:
                # last_name = sorted(pic_names)[-1]
                # file_name_number = int(re.findall(r'\d+',last_name)[0])
                return ('screenshot' + str(len(pic_names)+1) + '.png')
            else:
                return ('screenshot0.png')
        except Exception as e:
            raise RuntimeError(e)
    
    def connect(self):
        try:
            params = importlib.import_module(f'.{self.model.lower()}', package='pi.scope')
            func = getattr(params, self.model.capitalize())
            self.dso = func()
            self.visa.open_instr()
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)
        else:
            logger.info(f'Connect to {self.get_info()} successful!')
    
    def disconnect(self):
        try:
            self.visa.close_instr()
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)
        else:
            logger.info(f'{self.info} Disconnected!')
    
    def get_screen_shot(self):
        try:
            return self.dso.save_screenshot(visa=self.visa, file_name=self.gen_file_name())
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)
    
    def get_info(self):
        try:
            self.info = self.dso.get_info(visa=self.visa)
        except IOError as e:
            raise IOError(e)
        except RuntimeError as ee:
            raise RuntimeError(ee)
        else:
            return self.info



