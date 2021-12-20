
from unittest.mock import patch, Mock
from pi.power_control import PowerSupply
import pytest


@patch('serial.Serial.read_until')
@patch('pi.powerSupply.citric.Citric.try_opc', Mock())
def test_connect(mocker):
    instr = PowerSupply(model='citric',addr=34)
    instr.connect()
    assert instr.connect() == {'status': 'ok'}

@patch('serial.Serial.read_until',return_value=b'123\n')
@patch('pi.powerSupply.citric.Citric.try_opc', Mock())
def test_get_info(mocker):
    instr = PowerSupply(model='citric',addr=34)
    instr.connect()
    assert instr.get_info() == b'123\n'

@patch('serial.Serial.read_until',return_value=b'2\n')
def test_set_voltage(mocker):
    instr = PowerSupply(model='citric',addr=34)
    instr.connect()
    with pytest.raises(IOError):
        assert instr.set_voltage(voltage=24)

@patch('serial.Serial.read_until',return_value=b'1\n')
def test_set_voltage(mocker):
    instr = PowerSupply(model='citric',addr=34)
    instr.connect()
    assert instr.set_voltage(voltage=24) == {'status': 'ok'}
