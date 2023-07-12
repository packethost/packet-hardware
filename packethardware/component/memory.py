from .. import utils
from lxml import etree

from .component import Component


class Memory(Component):
    @classmethod
    def list(cls, lshw):
        xpath = etree.XPath("//node[description='System Memory']/node")

        memorys = []

        for memory in xpath(lshw):
            if "[empty]" in utils.xml_ev(lshw, memory, "description"):
                continue
            memorys.append(cls(lshw, memory))

        return memorys

    def __init__(self, lshw, element):
        Component.__init__(self, lshw, element)

        self.data = {
            "slot": utils.xml_ev(lshw, element, "slot"),
            # "size" is reported in bytes, so divide by 1024^3 to get an accurate human-readable number
            "size": str(int(int(utils.xml_ev(lshw, element, "size")) / 1073741824))
            + "GB",
            "clock": int(utils.xml_ev(lshw, element, "clock")) / 1000000
            if utils.xml_ev(lshw, element, "clock")
            else "",
            "type": utils.get_dmidecode_prop(
                "0x" + utils.xml_ev(lshw, element, "@handle", True).split(":", 1)[1],
                "17",
                "type",
            ),
            "asset_tag": "Unknown",
        }

        self.name = utils.xml_ev(lshw, element, "description")
        self.model = utils.xml_ev(lshw, element, "product")
        self.vendor = utils.normalize_vendor(utils.xml_ev(lshw, element, "vendor"))
        self.serial = utils.xml_ev(lshw, element, "serial")
        self.firmware_version = "N/A"
