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

        if "unknown" in self.vendor.lower():
            self.vendor = utils.get_hardwarevendor_from_hostnamectl(self)

        self.serial = utils.get_mc_info("guid")

        self.data = {"aux": utils.get_mc_info("aux")}

        if "supermicro" in self.vendor.lower():
            self.data["tty"] = utils.get_supermicro_serial_port_settings(self)
            self._set_tty_port_guess()
        elif "dell" in self.vendor.lower():
            self.data["tty"] = utils.get_dell_bios_serial_comm_settings(self)
            self._set_tty_port_guess()
        else:
            pass

    def _set_tty_port_guess(self):
        serial_comm = self.data["tty"].get("SerialComm")
        out_of_band_mgmt_port = (
            self.data["tty"]
            .get("Serial Port Console Redirection", {})
            .get("Out-of-Band Mgmt Port")
        )

        if serial_comm == "OnConRedirCom1" or out_of_band_mgmt_port == "COM1":
            self.data["tty"]["ttyPortGuess"] = "ttyS1"

    @classmethod
    def list(cls, _):
        bmcs = []
        bmcs.append(cls())
        return bmcs
