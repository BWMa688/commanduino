"""
.. module:: CommandADS1115
   :platform: Windows, Unix
   :synopsis: Represents an ADS1115 ADC module.

.. moduleauthor:: Your Name <your.email@example.com>

"""

import time
from .commanddevice import CommandDevice

# Bonjour Information
BONJOUR_ID = 'ADS1115'
CLASS_NAME = 'CommandADS1115'

# Incoming (Level)
CMD_ANSWER_LEVEL = 'D'

# Outgoing (Read)
CMD_REQUEST_LEVEL = 'R'
CMD_SET_GAIN = 'G'
CMD_SET_CHANNEL = 'C'
CMD_INITIALIZE = 'Z'
CMD_INITIALIZE_HEADER = 'E'


class CommandADS1115(CommandDevice):
    """
    ADS1115 Arduino device.

    Base:
        CommandDevice
    """

    def __init__(self):
        CommandDevice.__init__(self)
        self.level = None
        self.initialization_code = None
        self.gain = None
        self.channel = None
        self.level_lock = self._create_lock()
        self.initialization_code_lock = self._create_lock()
        self.gain_lock = self._create_lock()
        self.channel_lock = self._create_lock()
        self.register_all_requests()

    def register_all_requests(self):
        """
        Registers all requests to the device.
        """
        self.register_request(
            CMD_REQUEST_LEVEL,
            CMD_ANSWER_LEVEL,
            'level',
            self.handle_level_command)

        self.register_request(
            CMD_INITIALIZE,
            CMD_INITIALIZE_HEADER,
            'initialization_code',
            self.handle_initialize,
            timeout=1.2,
        )

        self.register_request(
            CMD_SET_GAIN,
            CMD_ANSWER_LEVEL,
            'gain',
            self.handle_set_gain
        )

        self.register_request(
            CMD_SET_CHANNEL,
            CMD_ANSWER_LEVEL,
            'channel',
            self.handle_set_channel
        )

    def handle_initialize(self, *arg):
        """ Handles the sensor initialization command. """
        if arg[0]:
            self.initialization_code = int(arg[0])
            self.initialization_code_lock.ensure_released()

    def init(self):
        """ Initializes the sensor.

        Refer to self.initialization_code for checking if the initialization was successful.

        <sensor>.initialization_code is None - the device wasn't initialized, call get_initialization_code()
        <sensor>.initialization_code == 1 - the device is found and the communication was established successfully
        <sensor>.initialization_code == 0 - the device was not found or the communication cannot be established, please
            check the device datasheet for possible reasons
        Call get_initialization_code() to try again.
        """
        self.get_initialization_code()

        if self.initialization_code != 1:
            self.logger.error("Unable to connect to sensor!")

        # wait for sensor to stabilize
        time.sleep(1)

    def handle_level_command(self, *arg):
        """
        Handles the level command.

        Args:
            *arg: Variable Argument.
        """
        if arg[0]:
            self.level = int(arg[0])
            self.level_lock.ensure_released()

    def get_level(self):
        """ Requests the ADC level from the device. """
        self.level_lock.ensure_locked()
        self.send_command(CMD_REQUEST_LEVEL)
        self.level_lock.wait()
        return self.level

    def handle_set_gain(self, *arg):
        """ Handles the gain setting command. """
        if arg[0]:
            self.gain = int(arg[0])
            self.gain_lock.ensure_released()

    def set_gain(self, gain):
        """ Sets the gain on the device. """
        self.gain_lock.ensure_locked()
        self.send_command(f"{CMD_SET_GAIN}{gain}")
        self.gain_lock.wait()
        return self.gain

    def handle_set_channel(self, *arg):
        """ Handles the channel setting command. """
        if arg[0]:
            self.channel = int(arg[0])
            self.channel_lock.ensure_released()

    def set_channel(self, channel):
        """ Sets the channel on the device. """
        self.channel_lock.ensure_locked()
        self.send_command(f"{CMD_SET_CHANNEL}{channel}")
        self.channel_lock.wait()
        return self.channel
