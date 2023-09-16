import typing

import pydantic

from cloud_latest.simplestreams.download import Download


class Release(pydantic.BaseModel):
    label: str = pydantic.Field(..., repr=False)
    dirname: str = pydantic.Field(..., alias="pubname")
    items: typing.Mapping[str, Download]
