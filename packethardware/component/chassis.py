from .. import utils
from .component import Component


class Chassis(Component):
    def __init__(self):
        Component.__init__(self)

        self.data = {}

        self.model = utils.get_fru_info("Chassis Part Number")
        self.serial = utils.get_fru_info("Chassis Serial")

    @classmethod
    def list(cls, _):
        chassis = []
        chassis.append(cls())
        return chassis
