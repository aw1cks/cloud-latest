from cloud_latest.image import CaseInsensitiveEnum


class CPUArchitecture(CaseInsensitiveEnum):
    # fmt: off
    I386    = ("i386", "x86",)
    AMD64   = ("amd64", "x86_64",)
    ARM64   = ("arm64",)
    ARMHF   = ("armhf",)
    PPC64EL = ("ppc64el",)
    RISCV64 = ("riscv64",)
    S390X   = ("s390x",)
    # fmt: on
