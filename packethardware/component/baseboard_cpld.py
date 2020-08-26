from .. import utils
from .component import Component


class BaseboardCPLD(Component):
    def __init__(self):
        Component.__init__(self)

        self.data = {}

        self.name = "Unknown"
        self.vendor = "Unknown"
        self.model = "Unknown"
        self.serial = "Unknown"
        self.firmware_version = utils.get_baseboard_cpld("firmware_version")

    @classmethod
    def list(cls, _):
        cpld = []
        cpld.append(cls())
        return cpld
