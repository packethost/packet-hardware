import re

from .component import Component
from .. import utils


class Disk(Component):
    @classmethod
    def list(cls, _):
        disks = []
        jsondisks, tool = utils.lsblk()
        for disk in jsondisks:
            if not disk["name"].startswith("/dev/sd") and not disk["name"].startswith(
                "/dev/nvme"
            ):
                continue
            disk["tool"] = tool
            disks.append(cls(disk))
        return disks

    # FS-1286 The API requires data for the disk size field to be in string format and
    # lsblk returns an integer value in the output.
    def __init__(self, lsblk):
        Component.__init__(self, lsblk, None)
        self.lsblk = lsblk
        self.data = {
            "size": str(self.__size()),
            "devname": self.lsblk["name"],
            "blockdevmodel": self.lsblk["model"].strip(),
            "rota": (
                self.lsblk["rota"]
                if isinstance(self.lsblk["rota"], str)
                else "1" if self.lsblk["rota"] else "0"
            ),
        }

        if self.__is_nvme():
            self.data["smart"] = utils.get_nvme_attributes(self.lsblk["name"])
        else:
            self.data["smart"] = utils.get_smart_attributes(self.lsblk["name"])

        match = re.search(r"^(\S+)_(\S+_\S+)", self.__getter("model"))
        if match:
            self.vendor = match.group(1)
            self.model = self.lsblk["model"].strip()
            self.name = match.group(1) + " " + match.group(2)
        else:
            self.model = self.__getter("model")
            self.name = self.model
            if self.lsblk["vendor"] is None:
                self.vendor = self.model.split(" ")[0]
            else:
                self.vendor = self.lsblk["vendor"].strip()

        self.serial = self.__getter("serial")
        self.firmware_version = self.__getter("firmware_version")

        if self.__is_megaraid():
            self.vendor = utils.get_smart_diskprop(self.lsblk["name"], "vendor")

        if self.vendor.strip() == "ATA":
            self.vendor = utils.normalize_vendor(self.model)
        else:
            self.vendor = utils.normalize_vendor(self.vendor)

    def __is_nvme(self):
        return self.lsblk["name"].startswith("/dev/nvme")

    def __is_megaraid(self):
        return self.lsblk["vendor"] in ("AVAGO", "PERC", "DELL", "LSI")

    def __getter(self, prop):
        if self.__is_nvme():
            return utils.get_nvme_diskprop(self.lsblk["name"], prop)
        elif self.__is_megaraid():
            return utils.get_smart_diskprop(self.lsblk["name"], prop)
        else:
            return utils.get_hdparm_diskprop(self.lsblk["name"], prop)

    def __size(self):
        if self.__is_megaraid():
            return utils.get_smart_diskprop(self.lsblk["name"], "size")
        else:
            return self.lsblk["size"]
