from .. import utils
from .component import Component


class ManagementController(Component):
    def __init__(self):
        Component.__init__(self)

        self.model = utils.dmidecode_string("system-product-name")
        self.firmware_version = utils.get_mc_info("firmware_version")

        if self.model == "Super Server":
            try:
                self.model = utils.get_fru_info("Board Part Number")
                self.name = utils.dmidecode_string("system-product-name")
            except Exception:
                utils.log(message="Something went wrong, probably no ipmitool.")
                self.firmware_version = ""
        elif self.model == "AS -1114S-WTRT":
            try:
                self.model = utils.get_fru_info("Board Part Number")
                self.name = utils.dmidecode_string("system-product-name")
                self.firmware_version = utils.get_mc_info("firmware_version")
            except Exception:
                utils.log(message="Something went wrong, probably no ipmitool.")
                self.firmware_version = ""
        else:
            self.name = self.model + " Base Management Controller"

        self.vendor = utils.normalize_vendor(utils.get_mc_info("vendor"))

        self.serial = utils.get_mc_info("guid")

        self.data = {"aux": utils.get_mc_info("aux")}

    @classmethod
    def list(cls, _):
        bmcs = []
        bmcs.append(cls())
        return bmcs
