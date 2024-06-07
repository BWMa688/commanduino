"""
.. module:: CommandADS1115
   :platform: Windows, Unix
   :synopsis: Represents an ADS1115 ADC module.

.. moduleauthor:: Bowen Ma <1395918273@qq.com>

"""
from .commanddevice import CommandDevice

import logging
module_logger = logging.getLogger(__name__)

# Bonjour Information
BONJOUR_ID = 'ADS1115'
CLASS_NAME = 'CommandADS1115'

# Incoming (Level)
CMD_ANSWER_ADC = 'A'

# Outgoing (Read)
CMD_REQUEST_ADC = 'RA'


class CommandADS1115(CommandDevice):

    def __init__(self):
        CommandDevice.__init__(self)
        self.register_all_requests()


    def register_all_requests(self):
        self.register_request(
            CMD_REQUEST_ADC,
            CMD_ANSWER_ADC,
            'adc',
            self.handle_adc_command)

    def handle_adc_command(self, *arg):
        if arg[0]:
            self.adc = float(arg[0])
            self.adc_lock.ensure_released()

