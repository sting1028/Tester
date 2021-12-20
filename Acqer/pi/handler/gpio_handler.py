import RPi.GPIO as GPIO
import logging
import time
logger = logging.getLogger(__name__)

class GpioHandler:
    def __init__(self, demo=False):
        GPIO.setmode(GPIO.BOARD)
        self.demo = demo
        self.pwm = None
        self.status_ok = {'status': 'ok'}
        self.table = {'UP': GPIO.PUD_UP, 'DOWN': GPIO.PUD_DOWN, 0: GPIO.LOW, 1: GPIO.HIGH, 'RIS':GPIO.RISING, 'FAL':GPIO.FALLING, 'BOTH':GPIO.BOTH}
    
    def setup_channel_in(self, pin:list, pud):
        """PUD: DOWN or UP -- pull up or pull down"""
        if not self.demo:
            try:
                GPIO.setup(pin, GPIO.IN, pull_up_down=self.table[pud.upper()])
                logger.info(f'GPIO:setup pin:{pin} for input with init {pud}')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok
    
    def setup_channel_out(self, pin:list, init):
        """init : 0 or 1"""
        if not self.demo:
            try:
                GPIO.setup(pin, GPIO.OUT, initial=self.table[init])
                logger.info(f'GPIO:setup pin :{pin} for output with init {init}')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok
    
    def release_channel(self, pin:list):
        if not self.demo:
            try:
                GPIO.cleanup(pin)
                logger.info(f'GPIO:pin{pin} released!')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok

    def read_channel(self, pin):
        if not self.demo:
            try:
                resp = GPIO.input(pin)
                logger.info(f'GPIO:read from pin:{pin} resp: {resp}')
                return resp
            except Exception as e:
                raise IOError(e)
        else:
            return 0
    
    def output_channel(self, pin:list, state):
        """state: 0 or 1"""
        if not self.demo:
            try:
                GPIO.output(pin, self.table[state])
                logger.info(f'GPIO:pin:{pin} has set by {state}')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok

    def wait_for_edge(self, pin, type, timeout):
        """GPIO.RISING, GPIO.FALLING or GPIO.BOTH"""
        if not self.demo:
            try:
                logger.info(f'GPIO:waiting for pin{pin} rising')
                GPIO.wait_for_edge(pin, self.table[type], timeout=timeout)
                logger.info(f'GPIO:pin{pin} have rising or timeout!')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            time.sleep(timeout)
            return self.status_ok

    def detected_for_edge(self, pin, type):
        """ GPIO.RISING, GPIO.FALLING or GPIO.BOTH"""
        if not self.demo:
            try:
                GPIO.add_event_detect(pin, self.table[type.upper()])
                logger.info(f'GPIO:pin{pin} have detected edge')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok

    def setup_channel_pwm(self, pin, freq):
        """only support pin 12,23,24,26"""
        if not self.demo:
            try:
                GPIO.setup(pin, GPIO.OUT)
                self.pwm = GPIO.PWM(pin, freq)
                logger.info(f'GPIO:pin{pin} have set up for pwm with freq:{freq}')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok
    
    def start_pwm(self, dc):
        """0.0 <= dc <= 100.0"""
        if not self.demo:
            try:
                self.pwm.start(dc)
                logger.info(f'GPIO:start pwm with duty cycle {dc}')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok

    def change_pwm_freq(self, freq):
        """freq is the new frequency in Hz"""
        if not self.demo:
            try:
                self.pwm.ChangeFrequency(freq)
                logger.info(f'GPIO:pwm changed the frequency to {freq}')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok
    
    def change_pwm_duty_cycle(self, dc):
        if not self.demo:
            """0.0 <= dc <= 100.0"""
            try:
                self.pwm.ChangeDutyCycle(dc)
                logger.info(f'GPIO:changed the duty cycle to {dc}')
                return self.status_ok
            except Exception as e:
                raise IOError(e)
        else:
            return self.status_ok

# if __name__ == '__main__':
#     a = GpioHandler()
#     pin = 16
#     a.setup_channel_in(pin=[pin], init='LOW')
#     a.release_channel([pin])
