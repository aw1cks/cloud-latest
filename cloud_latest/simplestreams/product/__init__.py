import datetime
import typing
from functools import cached_property

import pydantic

from cloud_latest.simplestreams.release import Release


class Product(pydantic.BaseModel):
    release_title: str
    release_codename: str
    version: str = pydantic.Field(..., repr=False)
    arch: str
    supported: bool
    support_eol: datetime.date

    @pydantic.computed_field  # type: ignore
    @cached_property
    def lts(self) -> bool:
        return "LTS" in self.release_title

    aliases: str = pydantic.Field(..., repr=False)
    os: str = pydantic.Field(..., repr=False)
    release: str = pydantic.Field(..., repr=False)
    versions: typing.Mapping[str, Release]

    def match_version(self, version: str) -> bool:
        """
        When providing 'version' input string:
          1. check if `release` (e.g. `jammy`) matched
          2. check if `release_codename` (e.g. `Jammy Jellyfish`) matched
          3. check if `release_title` (e.g. `22.04 LTS`) matched
          4. check if `version` (e.g. `22.04`) matched
        """
        # Let's make this case-insensitive
        v = version.lower()
        return any(
            [
                v == self.release.lower(),
                v == self.release_codename.lower(),
                v == self.release_title.lower(),
                v == self.version.lower(),
            ]
        )
