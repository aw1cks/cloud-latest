from typing import Sequence, Union

import aenum


class CaseInsensitiveEnum(aenum.Enum, settings=(aenum.MultiValue)):  # pyright: ignore
    @classmethod
    def _missing_name_(cls, name):
        # mypy doesn't know the enum is iterable
        # https://github.com/ethanfurman/aenum/issues/10
        # https://github.com/ethanfurman/aenum/issues/29
        for member in cls:  # type: ignore
            if member.name.lower() == name.lower():
                return member


class Platform(CaseInsensitiveEnum):
    # fmt: off
    AZURE   = ("vhd.tar.gz",)
    KVM     = ("disk-kvm.img", "uefi1.img",)
    LXD     = ("lxd.tar.xz",)
    VAGRANT = ("vagrant.box",)
    VMWARE  = ("ova", "vmdk",)
    WSL     = ("wsl.rootfs.tar.gz",)
    GENERIC = ("disk1.img", "tar.gz", "root.tar.gz", "root.tar.xz", "squashfs",)
    # fmt: on

def get_image_type(platform: Platform, image_type: str = "") -> str:
    if len(image_type) == 0:
        return platform.value

    platform_supported_image_types = platform.values
    if image_type not in platform_supported_image_types:
        errmsg = f"Platform '{platform.name}' does not support image type '{image_type}'"
        raise ValueError(errmsg)

    return image_type

class Image:
    _platform: Platform

    def __init__(
        self,
        platform: Union[str, Platform],
    ) -> None:
        self._platform = Platform(platform)

    @property
    def platform(self) -> Platform:
        return self._platform

    @property
    def suffixes(self) -> Sequence[str]:
        return self._platform.values
