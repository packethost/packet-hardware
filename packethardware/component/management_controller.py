from .. import utils
from .component import Component


class ManagementController(Component):
    def __init__(self):
        Component.__init__(self)

        self.data = {}

        self.model = utils.get_fru_info("Board Part Number")
        self.name = utils.dmidecode_string("system-product-name")

        self.vendor = utils.normalize_vendor(utils.get_mc_info("vendor"))

        if self.vendor == "Dell Inc.":
            try:
                self.firmware_version = utils.get_dell_management_fw_version("firmware_version")
            except:
                utils.log(message="Something went wrong, probably no racadm.")
                self.firmware_version = ""
        elif self.vendor == "Supermicro":
            try:
                self.firmware_version = utils.get_smc_management_fw_version("firmware_version")
            except:
                utils.log(message="Something went wrong, probably no ipmicfg.")
                self.firmware_version = ""
        else:
            self.firmware_version = ""

        self.serial = utils.get_mc_info("guid")

    @classmethod
    def list(cls, _):
        bmcs = []
        bmcs.append(cls())
        return bmcs
