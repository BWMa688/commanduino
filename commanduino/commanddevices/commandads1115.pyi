from .commanddevice import CommandDevice
from ..lock import Lock

class CommandADS1115(CommandDevice):
    adc_lock: Lock
    def get_adc(self) -> int: ...
    def handle_adc_command(self, *arg): ...
