import pathlib
from functools import cached_property
from typing import Optional

import pydantic

from cloud_latest.image import Platform


class Download(pydantic.BaseModel):
    ftype: str = pydantic.Field(..., repr=False)
    md5: str = pydantic.Field(..., repr=False)
    path: str = pydantic.Field(..., repr=False)
    sha256: str = pydantic.Field(..., repr=False)
    size: int = pydantic.Field(..., repr=False)

    # https://github.com/python/mypy/issues/14461
    # N.B. mypy does not allow decorators on top of property.
    # we are adding `type:ignore` for this reason.

    @pydantic.computed_field  # type: ignore
    @cached_property
    def file_name(self) -> str:
        """
        Strip the leading path, returning only the file name.
        """
        p = pathlib.Path(self.path)
        return p.name

    @pydantic.computed_field(repr=False)  # type: ignore
    @cached_property
    def manifest(self) -> bool:
        return self.ftype[-8:] == "manifest"

    @pydantic.computed_field  # type: ignore
    @cached_property
    def platform(self) -> Optional[str]:
        if not self.manifest:
            return Platform(self.ftype).name
